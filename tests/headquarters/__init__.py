import vcr


my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/headquarters/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)