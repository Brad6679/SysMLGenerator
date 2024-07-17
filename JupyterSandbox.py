import json
import cairosvg
from jupyter_client import KernelManager

#### Michael Shi's jupyter sandbox

class JupyterSandbox:
    def __init__(self, kernel_name):
        self.kernel_name = kernel_name
        self.km = None
        self.kc = None
        self.img = None

    def start_kernel(self):
        self.km = KernelManager(kernel_name=self.kernel_name)
        self.km.start_kernel()
        self.kc = self.km.client()
        self.kc.start_channels()
        self.kc.wait_for_ready()

    def execute_both(self, code, viz):
        self.kc.execute(code)
        self.kc.execute(viz)
        i = 0
        res = {}
        errors = ""       
        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=10)
                content = msg["content"]
                if "text" in content and "ERROR" in content["text"]:
                    print_error(content["text"])
                    errors += content["text"] + "\n"
                if "data" in content and "text/plain" in content["data"]:
                    res["text"] = content["data"]["text/plain"]
                    if "ERROR" in res["text"]:
                        print_error(res["text"])
                    else:
                        print("Output: ", res["text"])
                    i += 1

                if "data" in content and "image/svg+xml" in content["data"]:
                    res["img"] = content['data']['image/svg+xml']
                    self.img = content['data']['image/svg+xml']
                    i += 1

                if i == 2:
                    break
            except KeyboardInterrupt:
                print("Interrupted by user.")
                break
            except:
                break

        return errors

    def execute_code(self, code):
        msg_id = self.kc.execute(code)
        res = {}       
        while True:
            try:
                msg = self.kc.get_iopub_msg(timeout=10)
                content = msg["content"]
                if "data" in content and "text/plain" in content["data"]:
                    print("Text:", content["data"]["text/plain"])
                    res["text"] = content["data"]["text/plain"]
                if "data" in content and "image/svg+xml" in content["data"]:
                    res["img"] = content['data']['image/svg+xml']
                    self.img = content['data']['image/svg+xml']
                
            except KeyboardInterrupt:
                print("Interrupted by user.")
                break
            except:
                pass

            
    def save_image(self,name):
        print(self.img)
        try:
            cairosvg.svg2png(bytestring=self.img, write_to=f"imgs/{name}.png")
        except Exception as e:
            print(f"Error saving image: {str(e)}")

    def stop_kernel(self):
        self.kc.stop_channels()
        self.km.shutdown_kernel()
