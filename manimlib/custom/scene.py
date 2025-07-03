import os
import numpy as np
from manimlib.extract_scene import manim_config
from manimlib.custom.objects import ShaderMobject
from manimlib.utils.file_ops import guarantee_existence
from manimlib.custom.constants import FRAG_TEMPLATE, VERT_TEMPLATE
from manimlib.scene.interactive_scene import InteractiveScene


class ShaderScene(InteractiveScene):
    """
    An integration of Shaders with ManimGL.

    The path to the shader folder must be relative to the python script.

    |- some_folder
    |---- my_python_script.py
    |---- shader_folder
    |-------- frag.glsl
    |-------- vert.glsl
    |-------- geom.glsl (optional)

    If shader_folder is None (default), then shader folder is set to the SceneName.
    """

    shader_folder = None
    shader_class = ShaderMobject
    shader_directory = None         # Directory containing the shader folder
    uniforms = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._shader_initialised = False

        # to avoid using self.wait() repeatedly
        self.hold_on_wait = True

        # necessary files should exist
        self.assure_necessary_files_exist()
        self.init_shader()

        # some built-in uniforms like iTime, iResolution, iMouse
        # similar to Shadertoy
        self.init_uniforms()

    def setup(self) -> None:
        super().setup()
        self.add(self.shader)

    def assure_necessary_files_exist(self) -> None:
        self.shader_folder = self.shader_folder or self.__class__.__name__

        if self.shader_directory is None:
            scene_folder_path = os.path.dirname(
                os.path.abspath(manim_config.run.file_name)
            )
        else:
            scene_folder_path = self.shader_directory

        self.shader_folder_path = guarantee_existence(
            os.path.join(scene_folder_path, self.shader_folder)
        )

        for file_name in ["frag", "vert"]:
            file_name += ".glsl"
            filepath = os.path.join(self.shader_folder_path, file_name)

            if not os.path.exists(filepath):
                print(
                    f"\n!!File '{file_name}' Not Found!!\nGenerating '{file_name}' with default code template.\nFeel Free to change the code at anytime!!\n"
                )
                with open(filepath, "w") as f:
                    default_code = (
                        FRAG_TEMPLATE if file_name.startswith("frag") else VERT_TEMPLATE
                    )
                    f.write(default_code)

    def init_shader(self) -> None:
        self._shader_initialised = True
        self.shader = self.shader_class(shader_folder=self.shader_folder_path)

    def init_uniforms(self) -> None:
        scene_uniforms = lambda: self.get_uniforms()

        self.set_uniforms(scene_uniforms)

    def get_uniforms(self):
        resolution = manim_config.camera.resolution
        resolution = np.array(resolution, dtype=np.int32)

        base_uniforms = {
            "iTime": self.time,
            "iResolution": resolution,
            "iMouse": self.mouse_point.get_center()[:2],
        }

        if self.uniforms is None:
            return base_uniforms
        else:
            base_uniforms.update(self.uniforms)
            return base_uniforms

    def set_uniforms(self, uniforms) -> None:
        if isinstance(uniforms, dict):
            self.shader.set_uniforms(uniforms)
        else:
            self.shader.f_always.set_uniforms(uniforms)

    def refresh_shader(self) -> None:
        """
        In the embed mode, this can be called to refresh the code
        without any need to restart the Scene.
        """
        self.shader.refresh()

    def refresh_and_hold(self) -> None:
        """
        Refresh the Scene in loop.
        To exit the loop, press <spacebar> when Window is focused.
        """
        self.refresh_shader()
        self.hold_loop()

    def set_shader_folder(self, folder: str) -> None:
        # Is this really necessary?
        self.shader_folder = folder
        self.init_shader()


class CustomBackgroundScene(ShaderScene):
    shader_folder = 'background'
    shader_directory = r'C:\Users\abdal\AppData\Local\Programs\Python\Python312\Lib\site-packages\manimlib\custom'
    uniforms = dict(alpha = 0.125)