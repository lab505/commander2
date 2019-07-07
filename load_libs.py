import sys, platform, os

import mysql.connector

sys_name = platform.system().lower()

if sys_name.startswith('darwin'):  # mac
    import osgeo.ogr

os.environ['QGIS_DEBUG'] = '9'
if sys_name.startswith('darwin'):  # mac
    qgispath = '/Applications/QGIS3.app/Contents'
    qgis_pypath = qgispath + '/Resources/python'
    pyqt_plugins = qgispath + '/PlugIns'
    provider_path = qgispath + '/PlugIns/qgis'
    if qgis_pypath not in sys.path:
        sys.path = [qgis_pypath] + sys.path
elif sys_name.startswith('win'):  # windows
    qgispath = 'C:/Program Files/QGIS 3.6'
    pyqt_plugins = qgispath + '/apps/Qt5/plugins'
    provider_path = qgispath + '/apps/qgis/plugins'
    qgis_pypath = qgispath + '/apps/qgis/python'
    qgis_python_sitepkgspath = qgispath + '/apps/Python37/Lib/site-packages'
    if qgis_python_sitepkgspath not in sys.path:
        sys.path = [qgis_python_sitepkgspath] + sys.path
    if qgis_pypath not in sys.path:
        sys.path = [qgis_pypath] + sys.path
else:
    raise 'unknown system: %s' % sys_name

import qgis, qgis.core, qgis.gui, PyQt5, PyQt5.uic

if sys_name.startswith('win'):
    gdal_datapath = qgispath + '/share/gdal'
    # 解决 GDAL_DATA environment variable 报错
    os.environ['GDAL_DATA'] = gdal_datapath

if sys_name.startswith('darwin'):  # mac
    qgis.core.QgsApplication.setPrefixPath("/Applications/QGIS3.app/Contents/MacOS", True)
elif sys_name.startswith('win'):  # windows
    qgis.core.QgsApplication.setPrefixPath("C:/Program Files/QGIS 3.6/apps/qgis", True)
else:
    raise 'unknown system'

# 让QGIS输出错误日志
def write_log_message(message, tag, level):
    print ('{tag}({level}): {message}'.format(tag=tag, level=level, message=message))
qgis.core.QgsApplication.messageLog().messageReceived.connect(write_log_message)

if pyqt_plugins not in PyQt5.QtWidgets.QApplication.libraryPaths():
    # 解决 Could not find the Qt platform plugin 报错
    PyQt5.QtWidgets.QApplication.addLibraryPath(pyqt_plugins)

# 解决 No Data Providers 报错
qgis.core.QgsProviderRegistry.instance(provider_path)
