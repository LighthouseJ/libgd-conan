from conans import ConanFile, CMake, tools


class LibgdConan(ConanFile):
    name = "libgd"
    version = "2.2.4"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Libgd here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"

    def source(self):
        tools.download("https://github.com/libgd/libgd/releases/download/gd-%s/libgd-%s.tar.gz" % (self.version, self.version), 'gd.tar.gz')
        tools.untargz('gd.tar.gz')

        tools.replace_in_file("libgd-%s/CMakeLists.txt" % (self.version), "CMAKE_MINIMUM_REQUIRED(VERSION 2.6 FATAL_ERROR)", '''cmake_minimum_required (VERSION 3.6)
PROJECT(GD C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        tools.replace_in_file("libgd-%s/CMakeLists.txt" % (self.version), 'PROJECT(GD)', '# moved: PROJECT(GD)')
        
        tools.replace_in_file("libgd-%s/src/CMakeLists.txt" % (self.version), 'if (WIN32 AND NOT MINGW AND NOT MSYS)', 'if (BUILD_STATIC_LIBS AND WIN32 AND NOT MINGW AND NOT MSYS)')

    def build(self):
        cmake = CMake(self)
        cmake.definitions['BUILD_STATIC_LIBS'] = True
        cmake.configure(source_dir="%s/libgd-%s" % (self.source_folder, self.version))
        cmake.build()
        cmake.install()

        # Explicit way:
        # self.run('cmake %s/hello %s' % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)
        
    def package(self):
        self.copy("*", src="bin", dst="bin")
        self.copy("*", src="lib", dst="lib")
        self.copy("entities.h", dst="include", src="src")
        self.copy("gd.h",           dst="include", src="src")
        self.copy("gd_color_map.h", dst="include", src="src")
        self.copy("gd_errors.h",    dst="include", src="src")
        self.copy("gd_io.h",        dst="include", src="src")
        self.copy("gdcache.h",      dst="include", src="src")
        self.copy("gdfontg.h",      dst="include", src="src")
        self.copy("gdfontl.h",      dst="include", src="src")
        self.copy("gdfontmb.h",     dst="include", src="src")
        self.copy("gdfonts.h",      dst="include", src="src")
        self.copy("gdfontt.h",      dst="include", src="src")
        self.copy("gdfx.h",         dst="include", src="src")
        self.copy("gdpp.h",         dst="include", src="src")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if not self.options.shared:
            self.cpp_info.defines.append('NONDLL')
            self.cpp_info.defines.append('BGDWIN32')