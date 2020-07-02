QUESTION_TYPES = {
    0: 'SingleQuestion',
    3: 'MultyOptionsQuestion',
    4: 'NumericQuestion',
    5: 'DateTimeQuestion',
    6: 'GpsCoordinateQuestion',
    7: 'TextQuestion',
    9: 'TextListQuestion',
    10: 'QRBarcodeQuestion',
    11: 'MultimediaQuestion'
}

VARIABLE_TYPES = {
    3: 'Boolean'
}

ROSTER_TYPES = {
    1: 'Fixed set of items'
}


CLASSTYPE_MACRO = "System.Collections.Generic.Dictionary`2[[System.Guid, mscorlib],[WB.Core.SharedKernels.SurveySolutions.Documents.Macro, WB.Core.SharedKernels.Questionnaire]], mscorlib"  # noqa: E501
CLASSTYPE_LOOKUPTABLE = "System.Collections.Generic.Dictionary`2[[System.Guid, mscorlib],[WB.Core.SharedKernels.SurveySolutions.Documents.LookupTable, WB.Core.SharedKernels.Questionnaire]], mscorlib"  # noqa: E501
