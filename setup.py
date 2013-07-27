#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import platform

from distutils.core import setup
from distutils.core import Extension


def sources():
    cpp_files = []
    for dirpath, dirnames, filenames in os.walk('src'):
        for filename in filenames:
            if filename.endswith('.cpp'):
                cpp_files.append(os.path.join(dirpath, filename))
    return cpp_files

ext = {}
ext['sources'] = sources()

if sys.platform == 'win32':
    java_home = os.getenv('JAVA_HOME')
    if not java_home:
        print 'Environment Variable JAVA_HOME must be set.'
        sys.exit(-1)
    ext['libraries'] = ['Advapi32']
    ext['library_dir'] = [os.path.join(java_home, 'lib')]
    ext['define_macros'] = [('WIN32', 1)]
    ext['extra_compile_args'] = ['/EHsc']
    ext['include_dirs'] = [
        'src/native/common/include',
        'src/native/python/include',
        os.path.join(java_home, 'include'),
        os.path.join(java_home, 'include', 'win32')
    ]
elif sys.platform == 'darwin':
    # Changes according to:
    # http://stackoverflow.com/questions/8525193/cannot-install-jpype-on-os-x-lion-to-use-with-neo4j
    # and
    # http://blog.y3xz.com/post/5037243230/installing-jpype-on-mac-os-x
    osx = platform.mac_ver()[0][:4]
    java_home = os.getenv('JAVA_HOME')
    if not java_home:
        print "No JAVA_HOME Environment Variable set. Trying to guess it..."
        java_home = '/Library/Java/Home'
    if osx == '10.6':
        # I'm not sure if this really works on all 10.6 - confirm please :)
        java_home = ('/Developer/SDKs/MacOSX10.6.sdk/System/Library/'
                     'Frameworks/JavaVM.framework/Versions/1.6.0/')
    elif osx in ('10.7', '10.8'):
        java_home = ('/System/Library/Frameworks/JavaVM.framework/'
                     'Versions/Current/')
    ext['libraries'] = ['dl']
    ext['library_dir'] = [os.path.join(java_home, 'Libraries')]
    ext['define_macros'] = [('MACOSX', 1)]
    ext['include_dirs'] = [
        'src/native/common/include',
        'src/native/python/include',
        os.path.join(java_home, 'Headers'),
    ]
else:
    java_home = os.getenv('JAVA_HOME')
    if not java_home:
        print "No JAVA_HOME Environment Variable set. Trying to guess it..."
        possible_homes = [
            '/usr/lib/jvm/default-java',
            '/usr/lib/jvm/java-6-sun',
            '/usr/lib/jvm/java-1.5.0-gcj-4.4',
            '/usr/lib/jvm/jdk1.6.0_30',
            '/usr/lib/jvm/java-1.5.0-sun-1.5.0.08',
            '/usr/java/jdk1.5.0_05',
            '/usr/lib/jvm/java-6-openjdk-amd64',   # xubuntu 12.10
            '/usr/lib/jvm/java-7-openjdk-amd64'    # java 7 ubuntu 12.04
        ]
        for home in possible_homes:
            include_path = os.path.join(home, 'include')
            if os.path.exists(include_path):
                java_home = home
                break
        else:
            raise RuntimeError(
                "No Java/JDK could be found. I looked in the following "
                "directories: \n\n%s\n\nPlease check that you have it "
                "installed.\n\nIf you have and the destination is not in the "
                "above list please consider opening a ticket or creating a "
                "pull request on github: https://github.com/originell/jpype/"
                % '\n'.join(possible_homes))

    ext['libraries'] = ['dl']
    ext['library_dir'] = [os.path.join(java_home, 'lib')]
    ext['include_dirs'] = [
        'src/native/common/include',
        'src/native/python/include',
        os.path.join(java_home, 'include'),
        os.path.join(java_home, 'include', 'linux'),
        os.path.join(java_home, '..', 'include'),
        os.path.join(java_home, '..', 'include', 'linux'),
    ]

jpypeLib = Extension(name='_jpype',
                     sources=ext.get('sources'),
                     libraries=ext.get('libraries'),
                     define_macros=ext.get('define_macros'),
                     include_dirs=ext.get('include_dirs'),
                     library_dirs=ext.get('library_dir'),
                     extra_compile_args=ext.get('extra_compile_args'),
                    )

setup(
    name='JPype1',
    version='0.5.4.3',
    description='Friendly jpype fork with focus on easy installation.',
    author='Steve Menard',
    author_email='devilwolf@users.sourceforge.net',
    maintainer='Luis Nell',
    maintainer_email='cooperate@originell.org',
    url='https://github.com/originell/jpype/',
    packages=[
        'jpype', 'jpype.awt', 'jpype.awt.event', 'jpypex', 'jpypex.swing'],
    package_dir={
        'jpype': 'src/python/jpype',
        'jpypex': 'src/python/jpypex',
    },
    ext_modules=[jpypeLib],
)