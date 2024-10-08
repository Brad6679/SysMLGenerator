#import nbformat as nbf
import nbformat
import os
import cairosvg

"""
Class to run, edit, and retrieve output of SysMLv2 code in Jupyter Notebook
"""
class JupyterBook:
    """ 
      Initializes Jupyter Notebook
    """
    def __init__(self):
        # Create a new notebook
        self.nb = nbformat.v4.new_notebook()


    """ 
      Runs and retrieves output of code

      code : str
        SysMLv2 code to run

       viz : str
           Visualization command to run

        Returns : dict
            Dictionary of output cells (errors or image/return code)
    """
    def runCode(self, code, viz):
        self.nb.cells.append(nbformat.v4.new_code_cell(code))
        self.nb.cells.append(nbformat.v4.new_code_cell(viz))

        # Write the notebook to a file
        with open("output/sysml_notebook.ipynb", 'w') as f:
            nbformat.write(self.nb, f)

        # subprocess: jupyter nbconvert --to notebook --execute --inplace sysml_notebook.ipynb
        cmd = "jupyter nbconvert --to notebook --ExecutePreprocessor.kernel_name=sysml --execute --inplace output/sysml_notebook.ipynb"
        os.system(cmd)

        # Load the executed notebook
        with open("output/sysml_notebook.ipynb") as f:
            self.nb = nbformat.read(f, as_version=4)

        # Collect errors
        return self.nb.cells
    




'''
Testing
notebook = JupyterBook()

code = """
package 'UGVforLandmineDetection' {
	
	part def UnmannedGroundVehicle {
		port takeCommand;
		part def VehicleDriveandPowerSystem {
			port twist;
			part def CommunicationUnit {
				port next;
			}
			part def SensorArray {
				port def RevealSignalsBodyScan;
			}
		}
	}
}
"""
pind = code.find("package")
bind = code.find("{", pind)
name = code[pind + len("package"):bind].strip()
viz = f'%viz --view=tree {name}'
print(viz)
svg_content = notebook.runCode(code, viz)[1]['outputs'][0]['data']['image/svg+xml']

print(svg_content)

cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to='output.png')'''
