extends Node3D
## Loads every `.glb` in this folder and lets you orbit around them.
##
## `build.js` copies its output here, so the loop is: write a recipe, `npm run build`, press
## Play, look at the thing. An AI can tell you a mesh compiled; only you can tell whether it
## reads correctly at play size.
##
## Controls:
##   Left-drag        orbit          Wheel / +,-   zoom
##   Right-drag       pan            F             frame the current model
##   Left / Right     previous / next model        R  reload from disk
##   G                toggle the ground grid       W  toggle wireframe
##   Esc              quit

## Degrees of orbit per pixel of mouse movement.
@export var orbit_sensitivity: float = 0.4
## Fraction of the current distance added or removed per scroll notch.
@export var zoom_step: float = 0.12
## How much of the viewport height a freshly framed model should fill (0–1).
@export var frame_fill: float = 0.62
## Vertical angle limits, in degrees, to stop the camera flipping over the poles.
@export var pitch_limit_deg: float = 89.0

const CHARACTER_HEIGHT := 1.0  ## The modelkit's size reference, drawn for scale comparison.

var _models: Array[String] = []
var _index: int = 0
var _current: Node3D = null

var _yaw: float = 0.45
var _pitch: float = 0.35
var _distance: float = 3.0
var _target: Vector3 = Vector3.ZERO

var _camera: Camera3D
var _label: Label
var _grid: Node3D
var _scale_ref: Node3D
var _wireframe: bool = false


func _ready() -> void:
	_build_environment()
	_build_ui()
	_refresh_model_list()
	_load_current()


func _refresh_model_list() -> void:
	_models.clear()
	var dir := DirAccess.open("res://")
	if dir == null:
		push_error("Could not open res://")
		return
	dir.list_dir_begin()
	var name := dir.get_next()
	while name != "":
		if not dir.current_is_dir() and name.get_extension().to_lower() == "glb":
			_models.append(name)
		name = dir.get_next()
	dir.list_dir_end()
	_models.sort()
	_index = clampi(_index, 0, maxi(_models.size() - 1, 0))


func _load_current() -> void:
	if _current != null:
		_current.queue_free()
		_current = null

	if _models.is_empty():
		_set_status("No .glb files here.\nRun `npm run build` in model-generation/, then press R.")
		return

	var file := _models[_index]
	var scene: PackedScene = load("res://%s" % file)
	if scene == null:
		_set_status("Failed to load %s" % file)
		return

	_current = scene.instantiate() as Node3D
	add_child(_current)
	_apply_wireframe(_current)
	_frame_current()
	_set_status("%s   [%d/%d]" % [file, _index + 1, _models.size()])


## Bounding box of every mesh under `node`, in world space.
func _model_aabb(node: Node3D) -> AABB:
	var box := AABB()
	var seeded := false
	var stack: Array[Node] = [node]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var mesh := n as MeshInstance3D
		if mesh == null or mesh.mesh == null:
			continue
		var world := mesh.global_transform * mesh.mesh.get_aabb()
		if seeded:
			box = box.merge(world)
		else:
			box = world
			seeded = true
	return box if seeded else AABB(Vector3.ZERO, Vector3.ONE)


func _frame_current() -> void:
	if _current == null:
		return
	var box := _model_aabb(_current)
	_target = box.get_center()
	var radius := maxf(box.size.length() * 0.5, 0.05)
	var fov_rad := deg_to_rad(_camera.fov) * frame_fill
	_distance = radius / maxf(tan(fov_rad * 0.5), 0.01)


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		var motion := event as InputEventMouseMotion
		if motion.button_mask & MOUSE_BUTTON_MASK_LEFT:
			_yaw -= deg_to_rad(motion.relative.x * orbit_sensitivity)
			_pitch = clampf(
				_pitch - deg_to_rad(motion.relative.y * orbit_sensitivity),
				-deg_to_rad(pitch_limit_deg),
				deg_to_rad(pitch_limit_deg)
			)
		elif motion.button_mask & MOUSE_BUTTON_MASK_RIGHT:
			var right := _camera.global_transform.basis.x
			var up := _camera.global_transform.basis.y
			var pan := _distance * 0.0015
			_target -= (right * motion.relative.x - up * motion.relative.y) * pan
		return

	if event is InputEventMouseButton and event.is_pressed():
		var button := event as InputEventMouseButton
		if button.button_index == MOUSE_BUTTON_WHEEL_UP:
			_zoom(-1.0)
		elif button.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			_zoom(1.0)
		return

	if not (event is InputEventKey and event.is_pressed() and not event.is_echo()):
		return

	match (event as InputEventKey).keycode:
		KEY_RIGHT, KEY_D:
			_step_model(1)
		KEY_LEFT, KEY_A:
			_step_model(-1)
		KEY_R:
			_refresh_model_list()
			_load_current()
		KEY_F:
			_frame_current()
		KEY_G:
			_grid.visible = not _grid.visible
			_scale_ref.visible = _grid.visible
		KEY_W:
			_wireframe = not _wireframe
			if _current != null:
				_apply_wireframe(_current)
		KEY_EQUAL, KEY_KP_ADD:
			_zoom(-1.0)
		KEY_MINUS, KEY_KP_SUBTRACT:
			_zoom(1.0)
		KEY_ESCAPE:
			get_tree().quit()


func _step_model(delta: int) -> void:
	if _models.is_empty():
		return
	_index = wrapi(_index + delta, 0, _models.size())
	_load_current()


func _zoom(direction: float) -> void:
	_distance = clampf(_distance * (1.0 + zoom_step * direction), 0.05, 500.0)


func _process(_delta: float) -> void:
	var offset := Vector3(
		cos(_pitch) * sin(_yaw),
		sin(_pitch),
		cos(_pitch) * cos(_yaw)
	) * _distance
	_camera.global_position = _target + offset
	_camera.look_at(_target, Vector3.UP)


func _apply_wireframe(root: Node3D) -> void:
	var override: StandardMaterial3D = null
	if _wireframe:
		override = StandardMaterial3D.new()
		override.albedo_color = Color(0.45, 0.95, 0.85)
		override.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		var mesh := n as MeshInstance3D
		if mesh != null:
			mesh.material_override = override
	RenderingServer.set_debug_generate_wireframes(_wireframe)
	var vp := get_viewport()
	vp.debug_draw = (
		Viewport.DEBUG_DRAW_WIREFRAME if _wireframe else Viewport.DEBUG_DRAW_DISABLED
	)


func _build_environment() -> void:
	_camera = Camera3D.new()
	_camera.fov = 45.0
	_camera.near = 0.01
	add_child(_camera)

	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-45.0, -30.0, 0.0)
	sun.light_energy = 1.1
	sun.shadow_enabled = true
	add_child(sun)

	var fill := DirectionalLight3D.new()
	fill.rotation_degrees = Vector3(-20.0, 140.0, 0.0)
	fill.light_energy = 0.35
	add_child(fill)

	var env := Environment.new()
	env.background_mode = Environment.BG_COLOR
	env.background_color = Color(0.09, 0.10, 0.13)
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color(0.45, 0.50, 0.60)
	env.ambient_light_energy = 0.55
	var world := WorldEnvironment.new()
	world.environment = env
	add_child(world)

	_grid = _make_grid()
	add_child(_grid)

	_scale_ref = _make_scale_reference()
	add_child(_scale_ref)


## A 1x1 metre grid on the ground plane — the modelkit sizes everything in character heights,
## so a visible unit grid is the fastest way to catch a scale error.
func _make_grid() -> Node3D:
	var mesh := ImmediateMesh.new()
	var material := StandardMaterial3D.new()
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	material.vertex_color_use_as_albedo = true
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA

	mesh.surface_begin(Mesh.PRIMITIVE_LINES, material)
	var extent := 10
	for i in range(-extent, extent + 1):
		var major := i == 0
		var col := Color(0.45, 0.55, 0.70, 0.85) if major else Color(0.30, 0.34, 0.42, 0.45)
		mesh.surface_set_color(col)
		mesh.surface_add_vertex(Vector3(float(i), 0.0, float(-extent)))
		mesh.surface_set_color(col)
		mesh.surface_add_vertex(Vector3(float(i), 0.0, float(extent)))
		mesh.surface_set_color(col)
		mesh.surface_add_vertex(Vector3(float(-extent), 0.0, float(i)))
		mesh.surface_set_color(col)
		mesh.surface_add_vertex(Vector3(float(extent), 0.0, float(i)))
	mesh.surface_end()

	var node := MeshInstance3D.new()
	node.mesh = mesh
	return node


## A translucent human-height capsule off to one side, because "does this read beside a person"
## is the only scale question that matters.
func _make_scale_reference() -> Node3D:
	var capsule := CapsuleMesh.new()
	capsule.height = CHARACTER_HEIGHT
	capsule.radius = CHARACTER_HEIGHT * 0.13

	var material := StandardMaterial3D.new()
	material.albedo_color = Color(0.55, 0.70, 0.95, 0.30)
	material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	capsule.material = material

	var node := MeshInstance3D.new()
	node.mesh = capsule
	node.position = Vector3(CHARACTER_HEIGHT * 1.2, CHARACTER_HEIGHT * 0.5, 0.0)
	return node


func _build_ui() -> void:
	var layer := CanvasLayer.new()
	add_child(layer)

	_label = Label.new()
	_label.position = Vector2(16.0, 12.0)
	_label.add_theme_color_override("font_color", Color(0.90, 0.94, 1.0))
	_label.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.8))
	_label.add_theme_constant_override("outline_size", 4)
	layer.add_child(_label)

	var help := Label.new()
	help.anchor_top = 1.0
	help.anchor_bottom = 1.0
	help.offset_top = -74.0
	help.offset_left = 16.0
	help.text = (
		"L-drag orbit   R-drag pan   wheel zoom   F frame\n"
		+ "←/→ model   R reload   G grid   W wireframe   Esc quit\n"
		+ "Blue capsule = 1 character height (the modelkit's size reference)"
	)
	help.add_theme_color_override("font_color", Color(0.70, 0.76, 0.86))
	help.add_theme_color_override("font_outline_color", Color(0, 0, 0, 0.8))
	help.add_theme_constant_override("outline_size", 4)
	layer.add_child(help)


func _set_status(text: String) -> void:
	if _label != null:
		_label.text = text
