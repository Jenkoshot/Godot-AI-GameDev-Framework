extends SceneTree


func _init() -> void:
	var total_tests: int = 0
	var total_failures: Array[String] = []
	var dir: DirAccess = DirAccess.open("res://tests")
	if dir == null:
		push_error("Could not open res://tests")
		quit(1)
		return

	dir.list_dir_begin()
	var file_name: String = dir.get_next()
	while file_name != "":
		if file_name.begins_with("test_") and file_name.ends_with(".gd"):
			var script: GDScript = load("res://tests/%s" % file_name)
			var instance: TestCase = script.new()
			for method in script.get_script_method_list():
				var m_name: String = method["name"]
				if m_name.begins_with("test_"):
					total_tests += 1
					instance.failures.clear()
					instance.call(m_name)
					for f in instance.failures:
						total_failures.append("%s.%s: %s" % [file_name, m_name, f])
		file_name = dir.get_next()
	dir.list_dir_end()

	print("Ran %d test(s), %d failure(s)" % [total_tests, total_failures.size()])
	for f in total_failures:
		print("  FAIL: %s" % f)

	quit(0 if total_failures.is_empty() else 1)
