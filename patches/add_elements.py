import os
import shutil

import pyopenms

# Copy our modified `Elements.xml` to proper location inside `pyOpenMS` package
pyopenms_path = pyopenms.__path__[0]
source = "Elements.xml"
destination = os.path.join(pyopenms_path, "share/OpenMS/CHEMISTRY/Elements.xml")
dest = shutil.copyfile(source, destination)

