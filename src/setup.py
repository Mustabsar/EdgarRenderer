"""
Edgar(tm) Renderer was created by staff of the U.S. Securities and Exchange Commission.
Data and content created by government employees within the scope of their employment 
are not subject to domestic copyright protection. 17 U.S.C. 105.

To build Rendering Engine:
	
	c:\python33\python setup.py bdist-msi
	
	(results in subdirectory dist)
"""

import sys, os, datetime

ARELLEDIR = r"c:\re3\Arelle"

RE3_excluded_modules = [
    "arelle.CntlrQuickBooks",
    "arelle.CntlrWebMain",
    "arelle.CntlrWinMain",
    "arelle.CntlrWinTooltip",
    "arelle.DialogAbout",
    "arelle.DialogArcroleGroup",
    "arelle.DialogFind",
    "arelle.DialogFormulaParameters",
    "arelle.DialogLanguage",
    "arelle.DialogNewFactItem",
    "arelle.DialogOpenArchive",
    "arelle.DialogOpenTaxonomyPackage",
    "arelle.DialogPackageManager",
    "arelle.DialogPluginManager",
    "arelle.DialogRssWatch",
    "arelle.DialogURL",
    "arelle.DialogUserPassword",
    "arelle.UiUtil",
    "arelle.ViewWinConcepts",
    "arelle.ViewWinDTS",
    "arelle.ViewWinDiffs",
    "arelle.ViewWinFactGrid",
    "arelle.ViewWinFactList",
    "arelle.ViewWinFactTable",
    "arelle.ViewWinFormulae",
    "arelle.ViewWinGrid",
    "arelle.ViewWinList",
    "arelle.ViewWinProperties",
    "arelle.ViewWinRelationshipSet",
    "arelle.ViewWinRenderedGrid",
    "arelle.ViewWinRoleTypes",
    "arelle.ViewWinRssFeed",
    "arelle.ViewWinTests",
    "arelle.ViewWinTree",
    "arelle.ViewWinTupleGrid",
    "arelle.ViewWinVersReport",
    "arelle.ViewWinXml",
    "tcl",
    "gtk", # gui clipboard
]

setup_requires = ['lxml']
# install_requires specifies a list of package dependencies that are 
# installed when 'python setup.py install' is run. On Linux/Mac systems 
# this also allows installation directly from the github repository 
# (using 'pip install -e git+git://github.com/rheimbuchArelle.git#egg=Arelle') 
# and the install_requires packages are auto-installed as well.
install_requires = ['lxml']
options = {}
scripts = []
cxFreezeExecutables = []
cmdclass = {}

from distutils.command.build_py import build_py as _build_py

# Files that should not be passed through 3to2 conversion
# in python 2.7 builds
build_py27_unmodified = [
    'arelle/webserver/bottle.py',
    'arelle/PythonUtil.py'
    ]
# Files that should be excluded from python 2.7 builds
build_py27_excluded = [
    'arelle/CntlrQuickBooks.py',
    'arelle/CntlrWinMain.py',
    'arelle/CntlrWinTooltip.py',
    'arelle/Dialog*.py',
    'arelle/UiUtil.py',
    'arelle/ViewWin*.py',
    'arelle/WatchRss.py'
    ]

def match_patterns(path, pattern_list=[]):
    from fnmatch import fnmatch
    for pattern in pattern_list:
        if fnmatch(path, pattern):
            return True
    return False

# When building under python 2.7, run refactorings from lib3to2
# class build_py27(_build_py):
#     def __init__(self, *args, **kwargs):
#         _build_py.__init__(self, *args, **kwargs)
#         import logging
#         from lib2to3 import refactor
#         import lib3to2.main
#         rt_logger = logging.getLogger("RefactoringTool")
#         rt_logger.addHandler(logging.StreamHandler())
#         fixers = refactor.get_fixers_from_package('lib3to2.fixes')
#         fixers.remove('lib3to2.fixes.fix_print')
#         self.rtool = lib3to2.main.StdoutRefactoringTool(
#             fixers,
#             None,
#             [],
#             False,
#             False
#             )
#     
#     def copy_file(self, source, target, preserve_mode=True):
# 
#         if match_patterns(source, build_py27_unmodified):
#             _build_py.copy_file(self, source, target, preserve_mode)
#         elif match_patterns(source, build_py27_excluded):
#             print("excluding: %s" % source)
#         elif source.endswith('.py'):
#             try:
#                 print("3to2 converting: %s => %s" % (source, target))
#                 with open(source, 'rt') as input:
#                     # ensure file contents have trailing newline
#                     source_content = input.read() + "\n"
#                     nval = self.rtool.refactor_string(source_content, source)
#                 if nval is not None:
#                     with open(target, 'wt') as output:
#                         output.write('from __future__ import print_function\n')
#                         output.write(str(nval))
#                 else:
#                     raise(Exception("Failed to parse: %s" % source))
#             except Exception as e:
#                 print("3to2 error (%s => %s): %s" % (source,target,e))

# if sys.version_info[0] < 3:
#     setup_requires.append('3to2')
#     # cmdclass allows you to override the distutils commands that are 
#     # run through 'python setup.py somecmd'. Under python 2.7 replace 
#     # the 'build_py' with a custom subclass (build_py27) that invokes 
#     # 3to2 refactoring on each python file as its copied to the build directory.
#     cmdclass['build_py'] = build_py27
# (Under python3 no commands are replaced, so the default command classes are used.)

try:
# Under python2.7, run build before running build_sphinx
    import sphinx.setup_command
    class build_sphinx_py27(sphinx.setup_command.BuildDoc):
        def run(self):
            self.run_command('build_py')
            # Ensure sphinx looks at the "built" arelle libs that
            # have passed through the 3to2 refactorings
            # in `build_py27`.
            sys.path.insert(0, os.path.abspath("./build/lib"))
            sphinx.setup_command.BuildDoc.run(self)
                
    if sys.version_info[0] < 3:
        setup_requires.append('3to2')
        setup_requires.append('sphinx')
        # do a similar override of the 'build_sphinx' command to ensure 
        # that the 3to2-enabled build command runs before calling back to 
        # the default build_sphinx superclass. 
        cmdclass['build_sphinx'] = build_sphinx_py27
        # There is also a python 2.x conditional switch in 'apidocs/conf.py' 
        # that sets sphinx to look at the 3to2 converted build files instead 
        # of the original unconverted source.
except ImportError as e:
    print("Documentation production by Sphinx is not available: %s" % e)


''' this section was for py2app which no longer works on Mavericks, switch below to cx_Freeze        
if sys.platform == 'darwin':
    from setuptools import setup, find_packages
    
    setup_requires.append('py2app')
    # Cross-platform applications generally expect sys.argv to
    # be used for opening files.
    
    plist = dict(CFBundleIconFile='arelle.icns', 
                 NSHumanReadableCopyright='(c) 2010-2013 Mark V Systems Limited') 

    # MacOS launches CntlrWinMain and uses "ARELLE_ARGS" to effect console (shell) mode
    options = dict(py2app=dict(app=['arelle/CntlrWinMain.py'], 
                               iconfile='arelle/images/arelle.icns', 
                               plist=plist, 
                               #
                               # rdflib & isodate egg files: rename .zip cpy lib & egg-info subdirectories to site-packages directory
                               #
                               includes=['lxml', 'lxml.etree',  
                                         'lxml._elementpath', 'pg8000', 
                                         'rdflib', 'rdflib.extras', 'rdflib.tools', 
                                         # more rdflib plugin modules may need to be added later
                                         'rdflib.plugins', 'rdflib.plugins.memory', 
                                         'rdflib.plugins.parsers', 
                                         'rdflib.plugins.serializers', 'rdflib.plugins.serializers.rdfxml', 'rdflib.plugins.serializers.turtle', 'rdflib.plugins.serializers.xmlwriter', 
                                         'rdflib.plugins.sparql', 
                                         'rdflib.plugins.stores', 
                                         'isodate', 'regex', 'gzip', 'zlib'])) 

    packages = find_packages('.')
    dataFiles = [
    #XXX: this breaks build on Lion/Py3.2  --mike 
    #'--iconfile', 
    ('config',['arelle/config/' + f for f in os.listdir('arelle/config')]),
    ('doc',['arelle/doc/' + f for f in os.listdir('arelle/doc')]),
    #('examples',['arelle/examples/' + f for f in os.listdir('arelle/examples')]),
    ('images',['arelle/images/' + f for f in os.listdir('arelle/images')]),
    #('examples/plugin',['arelle/examples/plugin/' + f for f in os.listdir('arelle/examples/plugin')]),
    #('examples/plugin/locale/fr/LC_MESSAGES',['arelle/examples/plugin/locale/fr/LC_MESSAGES/' + f for f in os.listdir('arelle/examples/plugin/locale/fr/LC_MESSAGES')]),
    #('plugin',['arelle/plugin/' + f for f in os.listdir('arelle/plugin')]),
    ('scripts',['arelle/scripts/' + f for f in os.listdir('arelle/scripts-macOS')]),
      ]
    for dir, subDirs, files in os.walk('arelle/locale'):
        dir = dir.replace('\\','/')
        dataFiles.append((dir[7:],
                          [dir + "/" + f for f in files]))
    cx_FreezeExecutables = []
#End of py2app defunct section
'''
if sys.platform in ('darwin', 'linux2', 'linux', 'sunos5'): # works on ubuntu with hand-built cx_Freeze
    from setuptools import find_packages 
    try:
        from cx_Freeze import setup, Executable  
        cx_FreezeExecutables = [ 
            Executable( 
                script="arelleGUI.pyw", 
                targetName="arelle"
                ), 
            Executable( 
                script="arelleCmdLine.py", 
                )                             
            ] 
    except:
        from setuptools import setup
        cx_FreezeExecutables = []

    packages = find_packages('.') 
    dataFiles = None 
    options = dict( build_exe =  { 
        "include_files": [('arelle/config','config'), 
                          ('arelle/doc','doc'), 
                          ('arelle/images','images'), 
                          ('arelle/locale','locale'), 
                          #('arelle/examples','examples'), 
                          #('arelle/examples/plugin','examples/plugin'), 
                          #('arelle/examples/plugin/locale/fr/LC_MESSAGES','examples/plugin/locale/fr/LC_MESSAGES'), 
                          #('arelle/plugin','plugin'), 
                          ('arelle/scripts-macOS' if sys.platform == 'darwin' else 'arelle/scripts-unix',
                           'scripts'),
                          ],
        #
        # rdflib & isodate egg files: rename .zip cpy lib & egg-info subdirectories to site-packages directory
        #
        "includes": ['lxml', 'lxml.etree', 'lxml._elementpath', 'pg8000', 'pymysql', 'pyodbc',
                     # note cx_Oracle isn't here because it is version and machine specific, ubuntu not likely working
                     'rdflib', 'rdflib.extras', 'rdflib.tools', 
                     # more rdflib plugin modules may need to be added later
                     'rdflib.plugins', 'rdflib.plugins.memory', 
                     'rdflib.plugins.parsers', 
                     'rdflib.plugins.serializers', 'rdflib.plugins.serializers.rdfxml', 'rdflib.plugins.serializers.turtle', 'rdflib.plugins.serializers.xmlwriter', 
                     'rdflib.plugins.sparql', 
                     'rdflib.plugins.stores', 
                     'isodate', 'regex', 'gzip', 'zlib'], 
        "packages": packages, 
        } ) 
    if sys.platform == 'darwin':
        options["bdist_mac"] = {"iconfile": 'arelle/images/arelle.icns',
                                "bundle_name": 'Arelle'}
        
    
elif sys.platform == 'win32':
    from setuptools import find_packages
    from cx_Freeze import setup, Executable 
    # py2exe is not ported to Python 3 yet
    # setup_requires.append('py2exe')
    # FIXME: this should use the entry_points mechanism
    sys.path.insert(0,ARELLEDIR)
    packages = find_packages('.')
    print ("Pythonpath={},Packages = {}".format(packages, sys.path))
    dataFiles = None
    win32includeFiles = [(os.path.join(ARELLEDIR,'arelle\\config'),'config'),
                         (os.path.join(ARELLEDIR,'arelle\\doc'),'doc'),
                         (os.path.join(ARELLEDIR,'arelle\\images'),'images'),
                         (os.path.join(ARELLEDIR,'arelle\\locale'),'locale'),
                         #(os.path.join(ARELLEDIR,'arelle\\examples'),'examples'),
                         #(os.path.join(ARELLEDIR,'arelle\\examples\\plugin'),'examples/plugin'),
                         #(os.path.join(ARELLEDIR,'arelle\\examples\\plugin\\locale\\fr\\LC_MESSAGES'),'examples/plugin/locale/fr/LC_MESSAGES'),
                         #(os.path.join(ARELLEDIR,'arelle\\plugin'),'plugin'),
                         (os.path.join(ARELLEDIR,'arelle\\scripts-windows'),'scripts'),
                         ('..\\svc_template', 'svc_template'),
                         ('..\\resources','resources')]
    if 'arelle.webserver' in packages:
        win32includeFiles.append('QuickBooks.qwc')
    options = dict( build_exe =  {
        "excludes": RE3_excluded_modules,
        "include_files": win32includeFiles,
        "include_msvcr": True, # include MSVCR100
        "icon": os.path.join(ARELLEDIR,'arelle\\images\\arelle16x16and32x32.ico'),
        "packages": packages,
        #
        # rdflib & isodate egg files: rename .zip cpy lib & egg-info subdirectories to site-packages directory
        #
        "includes": ['lxml', 'lxml.etree', 'lxml._elementpath', 
                     'gzip', 'zlib', #'isodate', 
                     # for RE libraries
                     # note that if any of these are an egg file which is a zip that file has to be unzipped for cx_freeze
                     # note that Pillow is not listed, I can't find a reference in the RE code                    
                     'cProfile', 'matplotlib', 'numpy', 'dateutil', 'six'], # 'pyparsing', 
        } )
   
    # windows uses arelleGUI.exe to launch in GUI mode, arelleCmdLine.exe in command line mode
    cx_FreezeExecutables = [
        #Executable(
        #        script="EdgarRenderer.py",
        #        #script="arelleGUI.pyw",
        #        base="Win32GUI",
        #        ),
        Executable(
                #script="arelleCmdLine.py",
                script="EdgarRenderer.py",
                )                            
        ]
else:  
    #print("Your platform {0} isn't supported".format(sys.platform)) 
    #sys.exit(1) 
    from setuptools import os, setup, find_packages
    packages = find_packages('.')
    dataFiles = [        
        ('config',['arelle/config/' + f for f in os.listdir('arelle/config')]),
        ]
    cx_FreezeExecutables = []

timestamp = datetime.datetime.utcnow()
setup(name='RE3',
      # for version use year.month.day.hour (in UTC timezone) - must be 4 integers for building
      version=timestamp.strftime("%Y.%m.%d"),
      # replace description for RE:
      description='An open source XBRL platform',
      # replace long_description for RE:
      long_description=open(os.path.join(ARELLEDIR,'README.md')).read(),
      author='arelle.org',
      author_email='support@arelle.org',
      url='http://www.arelle.org',
      download_url='http://www.arelle.org/download',
      cmdclass=cmdclass,
      include_package_data = True,   # note: this uses MANIFEST.in
      packages=packages,
      data_files=dataFiles,
      platforms = ['OS Independent'],
      license = 'Apache-2',
      keywords = ['xbrl'],
      classifiers = [
          'Development Status :: 1 - Active',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache-2 License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Operating System :: OS Independent',
          'Topic :: XBRL Validation and Versioning',
          ],
      scripts=scripts,
      entry_points = {
          'console_scripts': [
              'EdgarRenderer=EdgarRenderer:main',
              #'arelle=arelle.CntlrCmdLine:main',
              #'arelle-gui=arelle.CntlrWinMain:main',
          ]
      },
      setup_requires = setup_requires,
      install_requires = install_requires,
      options = options,
      executables = cx_FreezeExecutables,
     )
