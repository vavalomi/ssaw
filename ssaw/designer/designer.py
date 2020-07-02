import copy
import hashlib
import imghdr
import json
import os
import shutil
import tempfile
import uuid
import zipfile
from datetime import datetime

from .constants import CLASSTYPE_LOOKUPTABLE, CLASSTYPE_MACRO, QUESTION_TYPES


def export_questionnaire(obj, outfolder):
    obj.PublicKey = str(uuid.uuid4())
    tmppath = tempfile.gettempdir()
    subfolder = obj.Title + " (" + obj.PublicKey + ")"
    path = os.path.join(tmppath, subfolder)
    filename = obj.Title + ".json"
    os.mkdir(path)
    tmpfile = os.path.join(path, filename)
    with open(tmpfile, "w") as outfile:
        json.dump(obj, outfile, cls=AutoJSONEncoder, indent=4, sort_keys=True)

    obj.export_lookuptables(path)
    obj.export_attachments(path)
    obj.export_translations(path)

    zipfile = os.path.join(outfolder, obj.Title)
    shutil.make_archive(zipfile, "zip", tmppath, subfolder)
    shutil.rmtree(path)


def import_questionnaire_json(jsonstring):
    return json.loads(jsonstring, object_hook=decode_object)


def import_questionnaire(archive):
    tmpdir = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    filename = ""
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(tmpdir)

    for root, dirs, files in os.walk(tmpdir):
        for file in files:
            if ".json" in file:
                filename = os.path.join(root, file)
                break

    lookupfolder = os.path.join(os.path.dirname(filename), "Lookup Tables")
    attachmentfolder = os.path.join(os.path.dirname(filename), "Attachments")
    translationfolder = os.path.join(os.path.dirname(filename), "Translations")

    with open(filename, "r") as fp:
        ret = json.load(fp, object_hook=decode_object)

    ret.import_lookuptables(lookupfolder)
    ret.import_attachments(attachmentfolder)
    ret.import_translations(translationfolder)

    shutil.rmtree(tmpdir)
    return ret


def clean_string(candidate):
    return candidate.replace("\n", " ").replace("\r", "").strip()


class MacrosCache:
    def __init__(self):
        self._list = {}

    def add(self, name, value):
        self._list[name] = value

    def evaluate(self, candidate):
        ret = candidate
        for name, value in self._list.items():
            ret = ret.replace("$" + name, value)
        return ret


def collect_expressions(obj, id="", evaluate_macros=False, macros_cache=None):  # noqa: C901
    ret = []
    if id == "":
        if hasattr(obj, "PublicKey"):
            id = obj.PublicKey
        else:
            try:
                show_structure(obj)
            except Exception:
                print(obj)
        if evaluate_macros and macros_cache is None:
            macros_cache = MacrosCache()

    if hasattr(obj, "Macros"):
        for key in obj.Macros:
            if key != "$type":
                m = obj.Macros[key]
                if "Content" in m:
                    cont = clean_string(m["Content"])
                    if cont:
                        name = m["Name"] if "Name" in m else "no_name"
                        if evaluate_macros:
                            macros_cache.add(name, cont)
                        else:
                            ret.append((id, "Macro", "", name, cont))

    if hasattr(obj, "StataExportCaption"):
        variablename = obj.StataExportCaption
    else:
        variablename = obj.Name if hasattr(obj, "Name") else ""
    if hasattr(obj, "ConditionExpression"):
        cont = clean_string(obj.ConditionExpression)
        if cont:
            if evaluate_macros:
                cont = macros_cache.evaluate(cont)
            ret.append((id, "Enablement", obj.PublicKey, variablename, cont))

    if hasattr(obj, "ValidationConditions"):
        for v in obj.ValidationConditions:
            if "Expression" in v:
                cont = clean_string(v["Expression"])
                if cont:
                    if evaluate_macros:
                        cont = macros_cache.evaluate(cont)
                    ret.append((id, "Validation", obj.PublicKey, variablename, cont))

    if hasattr(obj, "Expression"):  # variables
        cont = clean_string(obj.Expression)
        if cont:
            if evaluate_macros:
                cont = macros_cache.evaluate(cont)
            ret.append((id, "Variable", "", obj.Name, cont))

    if hasattr(obj, "Properties"):
        cont = ""
        if type(obj.Properties) is dict:
            if "OptionsFilterExpression" in obj.Properties:
                cont = clean_string(obj.Properties["OptionsFilterExpression"])
        else:
            if hasattr(obj.Properties, "OptionsFilterExpression"):
                cont = clean_string(obj.Properties.OptionsFilterExpression)

        if cont:
            if evaluate_macros:
                cont = macros_cache.evaluate(cont)
            ret.append((id, "Filter", obj.PublicKey, variablename, cont))

    if hasattr(obj, "Children"):
        for ch in obj.Children:
            a = collect_expressions(
                ch, id, evaluate_macros=evaluate_macros, macros_cache=macros_cache
            )
            if a:
                ret += a

    return ret


class AutoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj._json()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)


def decode_object(o):

    if "$type" in o:
        typevalue = o["$type"]
        del o["$type"]
    else:
        # some questionnaire documents don't have the proper type
        questionnaire_keys = [
            "CreatedBy",
            "CreationDate",
            "LastEventSequence",
            "SharedPersons",
            "UsesCSharp",
        ]
        if any(i in o for i in questionnaire_keys):
            typevalue = "QuestionnaireDocument"
        else:
            # extra info that we don't need
            extra_keys = [
                "ExpressionsPlayOrder",
                "DependencyGraph",
                "ValidationDependencyGraph",
            ]
            if all(i not in o for i in extra_keys):
                return o

    if typevalue in CLASS_DICT:
        if typevalue in [CLASSTYPE_LOOKUPTABLE, CLASSTYPE_MACRO]:
            o["$type"] = typevalue
            ret = create_object("MyDict", dict_type=typevalue, dict_obj=o)
        else:
            o["_Type"] = typevalue
            ret = create_object(typevalue, dict_obj=o)
    else:
        print(typevalue)
        print(o)
        raise TypeError

    return ret


def create_object(objtype, *args, **kwargs):
    if objtype in CLASS_DICT:
        obj = CLASS_DICT[objtype]()

        if "dict_obj" in kwargs:
            if objtype == "MyDict":
                obj = kwargs["dict_obj"]
            else:
                obj.import_dict(kwargs["dict_obj"])
        else:
            obj.create(*args, **kwargs)

        return obj
    else:
        raise AttributeError


def create_questionnaire(title, defaultsection=False):
    return create_object(
        "QuestionnaireDocument", title=title, defaultsection=defaultsection
    )


def question(questiontype=7, **kwargs):
    if questiontype in [0, 3, 4, 7]:
        q = create_object(
            QUESTION_TYPES[questiontype], questiontype=questiontype, **kwargs
        )
    else:
        q = create_object("Question", questiontype=questiontype, **kwargs)

    return q


def answer(value, text):
    return create_object("Answer", value, text)


def show_structure(obj, indent=0):
    print("-" * indent, obj._json())
    if hasattr(obj, "Children"):
        for item in obj.Children:
            show_structure(item, indent + 1)


class BaseClass(object):
    def import_dict(self, o):
        self.__dict__ = {**self.__dict__, **o}

    def _json(self):
        type = self.__dict__.get("_Type", self.__class__.__name__)
        ret = {"$type": type}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                ret[key] = value
        return ret


class Questionnaire(BaseClass):
    def __init__(self):
        self._Type = "QuestionnaireDocument"
        self.PublicKey = ""
        self.Title = ""
        self.CreationDate = datetime.utcnow().isoformat()
        self.CreatedBy = "00000000-0000-0000-0000-000000000000"
        self.HideIfDisabled = False
        self.Children = []
        self.Macros = create_object("MyDict", dict_type=CLASSTYPE_MACRO)
        self.Attachments = []
        self.LookupTables = create_object("MyDict", dict_type=CLASSTYPE_LOOKUPTABLE)
        self.Translations = []
        self.SharedPersons = []

    def create(self, title, defaultsection=True):
        self.Title = title
        if defaultsection:
            self.Children.append(create_object("Group", self))

    def add_section(self, title):
        self.Children.append(create_object("Group", self, title))
        return self.Children[-1]

    def add_macro(self, **kwargs):
        item = {str(uuid.uuid4()): create_object("Macro", **kwargs)}
        self.Macros.update(item)

    def add_lookuptable(self, **kwargs):
        item = {str(uuid.uuid4()): create_object("LookupTable", **kwargs)}
        self.LookupTables.update(item)

    def add_attachment(self, **kwargs):
        self.Attachments.append(create_object("Attachment", **kwargs))

    def add_translation(self, **kwargs):
        self.Translations.append(create_object("Translation", **kwargs))

    def export_translationtemplate(self, outfolder):
        pass

    def export_lookuptables(self, outfolder):
        if len(self.LookupTables.keys()) > 1:
            ff = os.path.join(outfolder, "Lookup Tables")
            os.mkdir(ff)
            for key in self.LookupTables:
                if key != "$type":
                    filename = key.replace("-", "") + ".txt"
                    filename = os.path.join(ff, filename)
                    with open(filename, "w") as f:
                        f.writelines(self.LookupTables[key]._FileContent)

    def import_lookuptables(self, infolder):
        for key in self.LookupTables:
            if key != "$type":
                filename = os.path.join(infolder, key.replace("-", "") + ".txt")
                if type(self.LookupTables[key]) == "LookupTable":
                    self.LookupTables[key].import_content(filename)

    def export_attachments(self, outfolder):
        if len(self.Attachments):
            ff = os.path.join(outfolder, "Attachments")
            os.mkdir(ff)
            for item in self.Attachments:
                itemfolder = os.path.join(ff, item.AttachmentId.replace("-", ""))
                os.mkdir(itemfolder)
                filename = os.path.join(itemfolder, item._FileName)
                with open(filename, "wb") as f:
                    f.write(item._FileContent)

                filename = os.path.join(itemfolder, "Content-Type.txt")
                with open(filename, "w") as f:
                    f.writelines("image/" + item._ImageType)

    def import_attachments(self, infolder):
        for item in self.Attachments:
            itemfolder = os.path.join(infolder, item.AttachmentId.replace("-", ""))
            for file in os.listdir(itemfolder):
                if file != "Content-Type.txt":
                    item.import_content(os.path.join(itemfolder, file))

    def export_translations(self, outfolder):
        if len(self.Translations):
            ff = os.path.join(outfolder, "Translations")
            os.mkdir(ff)
            for item in self.Translations:
                filename = os.path.join(ff, item.Id.replace("-", "") + ".xlsx")
                with open(filename, "wb") as f:
                    f.write(item._FileContent)

    def import_translations(self, infolder):
        for item in self.Translations:
            filename = os.path.join(infolder, item.Id.replace("-", "") + ".xlsx")
            item.import_content(filename)

    def variables(self, obj=None):
        if not obj:
            obj = self
        ret = {}
        if obj._Type in ["Group", "QuestionnaireDocument"]:
            for ch in obj.Children:
                chret = self.variables(ch)
                if chret:
                    ret.update(chret)
        elif obj._Type not in ["StaticText"]:
            ret = {obj.VariableName: obj}
        return ret


class Group(BaseClass):
    def create(
        self,
        parent,
        title="New Section",
        condition="",
        hideifdisabled=False,
        description="",
    ):
        self.__parent__ = parent
        self.PublicKey = str(uuid.uuid4())
        self.Title = title
        self.ConditionExpression = condition
        self.HideIfDisabled = hideifdisabled
        self.Description = description
        self.IsRoster = False
        self.RosterSizeSource = 0
        self.FixedRosterTitles = []
        self.Children = []

    def add_question(self, questiontype=7, **kwargs):
        return self.add_item(question(questiontype, **kwargs))

    def add_subsection(self, title):
        self.Children.append(create_object("Group", self, title))
        return self.Children[-1]

    def add_roster(self):
        pass

    def add_statictext(self, *args, **kwargs):
        self.add_item(create_object("StaticText", *args, **kwargs))

    def add_variable(self, *args, **kwargs):
        self.add_item(create_object("Variable", *args, **kwargs))

    def add_item(self, obj_q):
        ref = copy.deepcopy(obj_q)
        self.Children.append(ref)
        return ref


class FixedRosterTitle(object):
    def __init__(self, value=1, title="First Title", object=None):
        if object:
            self.__dict__ = {**self.__dict__, **object}
        else:
            self.Value = value
            self.Title = title


class QuestionFactory(BaseClass):
    def create(
        self,
        questiontext,
        questiontype,
        variablename="",
        variablelabel="",
        instructions="",
        questionscope=0,
        hideifdisabled=False,
    ):
        self.PublicKey = str(uuid.uuid4())
        self.HideIfDisabled = hideifdisabled
        self.Instructions = instructions
        self.QuestionScope = questionscope
        self.QuestionText = questiontext
        self.QuestionType = questiontype
        self.StataExportCaption = variablename
        self.VariableLabel = variablelabel
        self.Properties = create_object("QuestionProperties")
        self.ValidationConditions = []
        self._Type = QUESTION_TYPES[self.QuestionType]

    def add_validation(self, expression="", message="", v_obj=None):
        if v_obj is None:
            v_obj = create_object("ValidationCondition", expression, message)
        self.ValidationConditions.append(v_obj)


class TextQuestion(QuestionFactory):
    def create(self, mask="", **kwargs):
        self.Mask = mask
        super(TextQuestion, self).create(**kwargs)


class NumericQuestion(QuestionFactory):
    def create(self, isinteger=False, **kwargs):
        self.IsInteger = isinteger
        super(NumericQuestion, self).create(**kwargs)


class SingleQuestion(QuestionFactory):
    def create(self, combobox=False, cascading_parent=None, **kwargs):
        self.IsFilteredCombobox = combobox
        if cascading_parent:
            self.CascadeFromQuestionId = cascading_parent
        self.Answers = []
        super(SingleQuestion, self).create(**kwargs)

    def add_option(self, *args, **kwargs):
        self.Answers.append(answer(*args, **kwargs))


class MultyOptionsQuestion(SingleQuestion):
    def create(self, ordered=False, yesno=False, **kwargs):
        self.AreAnswersOrdered = ordered
        self.YesNoView = yesno
        super(MultyOptionsQuestion, self).create(**kwargs)


class TextListQuestion(QuestionFactory):
    def __init__(self, **kwargs):
        super(TextListQuestion, self).__init__(**kwargs)


class ValidationCondition(BaseClass):
    def create(self, expression, message):
        self.Expression = expression
        self.Message = message


class QuestionProperties(BaseClass):
    def create(self):
        self.HideInstructions = False
        self.UseFormatting = False
        self.OptionsFilterExpression = ""


class AnswerFactory(BaseClass):
    def create(self, value, text):
        self._Type = "Answer"
        self.PublicKey = str(uuid.uuid4())
        self.AnswerText = text
        self.AnswerValue = value


class StaticText(BaseClass):
    def create(self, text, hideifdisabled=False):
        self.PublicKey = str(uuid.uuid4())
        self.Text = text
        self.AttachmentName = ""
        self.HideIfDisabled = hideifdisabled
        self.ValidationConditions = []


class Variable(BaseClass):
    def __init__(self):
        self.PublicKey = str(uuid.uuid4())
        self.Name = ""
        self.Label = ""
        self.Type = 3
        self.Expression = ""
        self.VariableName = ""

    def create(self, name="", type=3, expression="", label=""):
        self.Name = name
        self.Label = label
        self.Type = type
        self.Expression = expression
        self.VariableName = name


class MyDict(dict):
    def create(self, dict_type):
        self.update({"$type": dict_type})


class Macro(BaseClass):
    def create(self, name, content, description=""):
        self.Name = name
        self.Content = content
        self.Description = description


class LookupTable(BaseClass):
    def create(self, tablename, filename, importcontent=True):
        self.TableName = tablename
        self.FileName = os.path.basename(filename)

        if importcontent:
            self.import_content(filename)

    def import_content(self, filename):
        with open(filename, "r") as f:
            self._FileContent = f.readlines()


class Attachment(BaseClass):
    def create(self, name, filename, importcontent=True):
        self.AttachmentId = str(uuid.uuid4())
        self.Name = name

        if importcontent:
            self.import_content(filename)

    def import_content(self, filename):
        with open(filename, "rb") as f:
            self._FileName = os.path.basename(filename)
            self._FileContent = f.read()
            self._ImageType = imghdr.what(filename)
            self.ContentId = hashlib.sha1(self._FileContent).hexdigest().upper()


class Translation(BaseClass):
    def create(self, name, filename, importcontent=True):
        self.Id = str(uuid.uuid4())
        self.Name = name

        if importcontent:
            self.Id = str(uuid.uuid4())
            self.import_content(filename)

    def import_content(self, filename):
        with open(filename, "rb") as f:
            self._FileContent = f.read()


CLASS_DICT = {
    "Group": Group,
    "Answer": AnswerFactory,
    "AreaQuestion": QuestionFactory,
    "Attachment": Attachment,
    "AudioQuestion": QuestionFactory,
    "Question": QuestionFactory,
    "QuestionnaireDocument": Questionnaire,
    "QuestionProperties": QuestionProperties,
    "StaticText": StaticText,
    "DateTimeQuestion": QuestionFactory,
    "GpsCoordinateQuestion": QuestionFactory,
    "MultimediaQuestion": QuestionFactory,
    "MultyOptionsQuestion": MultyOptionsQuestion,
    "NumericQuestion": NumericQuestion,
    "QRBarcodeQuestion": QuestionFactory,
    "SingleQuestion": SingleQuestion,
    "TextListQuestion": TextListQuestion,
    "TextQuestion": TextQuestion,
    "Translation": Translation,
    "ValidationCondition": ValidationCondition,
    "Variable": Variable,
    CLASSTYPE_LOOKUPTABLE: MyDict,
    CLASSTYPE_MACRO: MyDict,
    "Macro": Macro,
    "MyDict": MyDict,
    "LookupTable": LookupTable,
}
