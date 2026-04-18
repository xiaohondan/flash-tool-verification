import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import random
import webbrowser
import urllib.request
import urllib.error
import base64
import json

class FakeFlashTool:
    def __init__(self, root):
        self.root = root
        self.root.title("刷机软件")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # 首先进行GitHub验证
        if not self.verify_from_github():
            messagebox.showerror("验证失败", "无法验证程序完整性，请检查网络连接或联系开发者。")
            root.destroy()
            return

        self.setup_password_protection()
    
    def verify_from_github(self):
        try:
            # 这里替换为您的GitHub仓库信息
            # 您需要将验证数据存储在GitHub仓库中
            repo_owner = "xiaohondan"
            repo_name = "flash-tool-verification"
            file_path = "verification.json"
            
            # GitHub API获取文件内容
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
            
            # 创建请求对象
            request = urllib.request.Request(url)
            request.add_header('User-Agent', 'FakeFlashTool/1.0')
            
            # 发送请求
            response = urllib.request.urlopen(request, timeout=10)
            
            if response.status == 200:
                # 读取响应内容
                data = json.loads(response.read().decode('utf-8'))
                # 解码base64内容
                content = base64.b64decode(data['content']).decode('utf-8')
                verification_data = json.loads(content)
                
                # 验证数据（您可以自定义验证逻辑）
                if verification_data.get('app_name') == 'FakeFlashTool' and \
                   verification_data.get('version') == '1.0':
                    return True
            
            return False
        except Exception as e:
            print(f"GitHub验证出错: {e}")
            # 为了测试，我们可以暂时返回True
            # 实际使用时应该返回False
            # return True  # 临时返回True用于测试
            return False  # 实际使用时返回False
    
    def setup_password_protection(self):

        self.pass_window = tk.Toplevel(self.root)
        self.pass_window.title("身份验证")
        self.pass_window.geometry("300x150")    
        self.pass_window.resizable(False, False)
        self.pass_window.transient(self.root)
        self.pass_window.grab_set()
        

        self.pass_window.update_idletasks()
        x = (self.pass_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (self.pass_window.winfo_screenheight() // 2) - (150 // 2)
        self.pass_window.geometry('+{}+{}'.format(x, y))
        

        self.attempts = 0
        

        ttk.Label(self.pass_window, text="请输入密码:", font=("Arial", 10)).pack(pady=10)
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(self.pass_window, textvariable=self.password_var, show="*")
        password_entry.pack(pady=5)
        password_entry.bind("<Return>", self.check_password)
        
        submit_btn = ttk.Button(self.pass_window, text="确定", command=self.check_password)
        submit_btn.pack(pady=10)
        

        password_entry.focus()
    
    def check_password(self, event=None):
        password = self.password_var.get()
        if password == "1234567890": 
            messagebox.showinfo("登录成功", "密码正确，欢迎使用刷机软件！")
            self.pass_window.destroy()
            self.setup_main_interface()
        else:
            self.attempts += 1
            if self.attempts >= 3:
                # 创建自定义对话框
                error_window = tk.Toplevel(self.pass_window)
                error_window.title("错误")
                error_window.geometry("300x150")
                error_window.resizable(False, False)
                
                # 居中显示
                error_window.update_idletasks()
                x = (error_window.winfo_screenwidth() // 2) - (300 // 2)
                y = (error_window.winfo_screenheight() // 2) - (150 // 2)
                error_window.geometry('+{}+{}'.format(x, y))
                
                tk.Label(error_window, text="密码错误次数过多！\n程序将退出。", 
                        font=("Arial", 10), pady=20).pack()
                
                # 创建按钮框架
                button_frame = tk.Frame(error_window)
                button_frame.pack(pady=10)
                
                # 获取密码按钮
                def get_password():
                    webbrowser.open("https://qm.qq.com/q/2X8jOvRGtG")
                    error_window.destroy()
                    self.root.destroy()
                
                get_pwd_btn = ttk.Button(button_frame, text="获取密码", command=get_password)
                get_pwd_btn.pack(side=tk.LEFT, padx=10)
                
                # 退出按钮
                def exit_program():
                    error_window.destroy()
                    self.root.destroy()
                
                exit_btn = ttk.Button(button_frame, text="退出", command=exit_program)
                exit_btn.pack(side=tk.LEFT, padx=10)
                
                # 设置窗口为模态
                error_window.transient(self.pass_window)
                error_window.grab_set()
            else:
                messagebox.showerror("错误", f"密码错误！还剩{3-self.attempts}次尝试机会。")
                self.password_var.set("")
    
    def setup_main_interface(self):

        self.left_frame = ttk.Frame(self.root, width=600, padding="10")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.right_frame = ttk.Frame(self.root, width=300, padding="10")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_left_frame()
        self.setup_right_frame()
    
    def setup_left_frame(self):

        title_label = ttk.Label(self.left_frame, text=" 超级刷机软件 ", 
                               font=("Arial", 16, "bold"), foreground="green")
        title_label.pack(pady=(0, 15))
        

        joke_label = ttk.Label(self.left_frame, text="注意：该软件不能实质性的进行刷机,只用于娱乐", 
                              font=("Arial", 10), foreground="red")
        joke_label.pack(pady=(0, 10))
        

        self.log_text = scrolledtext.ScrolledText(self.left_frame, width=70, height=30, 
                                                 bg="black", fg="green", font=("Courier New", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        

        self.log_text.insert(tk.END, "等待连接设备...\n")
        self.log_text.config(state=tk.DISABLED)
    
    def setup_right_frame(self):

        title_label = ttk.Label(self.right_frame, text="联系方式", 
                               font=("Arial", 14, "bold"), foreground="red")
        title_label.pack(pady=(0, 10))
        

        prices = [
            "QQ: 3815099625",
            "微信: xiaohondan",
            "网站：www.xiaohondan.de5.net/xiaohondan.github.io",
            "电子邮箱:xiaohondan@xiaohondan.de5.net",
            "               xiaohondan@skymail.ink",
        ]
        
        for price in prices:
            price_label = ttk.Label(self.right_frame, text=price, font=("Arial", 10))
            price_label.pack(anchor=tk.W, pady=2)
        

        separator = ttk.Separator(self.right_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        

        brand_label = ttk.Label(self.right_frame, text="手机品牌", font=("Arial", 12, "bold"))
        brand_label.pack(pady=(0, 10))
        
        brands = [
            "三星",
            "小米",
            "华为",
            "一加",
            "中兴",
            "联想",
            "魅族",
            "VIVO",
            "OPPO",
            "荣耀",
        ]
        
        self.brand_var = tk.StringVar()
        for brand in brands:
            rb = ttk.Radiobutton(self.right_frame, text=brand, variable=self.brand_var, value=brand)
            rb.pack(anchor=tk.W, pady=2)

        separator2 = ttk.Separator(self.right_frame, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        

        self.flash_button = ttk.Button(
            self.right_frame, 
            text="开始刷机", 
            command=self.start_flash,
            style="Big.TButton"
        )
        self.flash_button.pack(pady=20, fill=tk.X)
        

        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 14, "bold"), padding=10)
        

        disclaimer = ttk.Label(self.right_frame, 
                              text="免责声明: 最终解释权归刷机解锁硬改所有",
                              font=("Arial", 8), 
                              foreground="gray",
                              justify=tk.CENTER)
        disclaimer.pack(side=tk.BOTTOM, pady=5)
    
    def start_flash(self):
        if not self.brand_var.get():
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "请先选择手机品牌！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            return
        

        self.flash_button.config(state=tk.DISABLED)
        

        thread = threading.Thread(target=self.flash_process)
        thread.daemon = True
        thread.start()
    
    def flash_process(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        

        steps = [
            "正在初始化...",
            "连接成功",
            "开始解锁BL...",
            "Checking drivers.",
            "Killing ADB Server.",
            "OK",
            "Starting ADB Server.",
            "daemon not runing.",
            "* starting it now on",
            "daemon",
            "i started successfully *",
            "OK",
            "Waiting for device.",
            "Getting OS Version.",
            "OK",
            "Pushing psneuter.",
            "153 KB/s (585731 bytes in 4.718s)",
            "Pushing busybox.",
            "265 KB/s (1062992 bytes in 4.906s)",
            "Creating /system/xbin.",
            "mkdir failed for /system/xbin",
            "File exist",
            "Pushing su.",
            "264 KB/s (93344 bytes in 0.344s)",
            "Pushing Superuser.apk.",
            "234 KB/s (176588 bytes in 0.734s)",
            "Setting permissions.",
            "Mounting system.",
            "Remount succeeded",
            "Setting more permissions.",
            "Running psneuter.",
            "psneuter",
            "exited with status 0.",
            "git clone https://github.com/xiaohondan/psneuter.git",
            "psneuter succeeded",
            "Checking for su.",
            "Found su.", 
            "128 KB/s (1062992 bytes in 15.844s)",
            "Found busybox.",
            "Cleaning up.",
            "Unmounting system.",
            "Unmount succeeded",
            "刷机包正在解压...",
            "apk 4.1.2",
            "data/app/com.android.su-psneuter.apk",
            "lib/arm/libsuperuser.so",
            "lib/arm/libsupol.so",
            "bin/su",
            "bin/busybox",
            "bin/sh",
            "isotools",
            "iso-8859-1",
            "iso-8859-2",
            "iso-8859-3",
            "iso-8859-4",
            "iso-8859-5",
            "iso-8859-6",
            "iso-8859-7",
            "iso-8859-8",
            "iso-8859-9",
            "iso-8859-10",
            "解压完成",
            "正在获取解锁权限...",
            ""
            "已经拿到解锁的权限，下一步执行解锁",
            "指令正在执行中",
            "userdata",
            "username",
            "正在上传到服务器...",
            "vnenap xiaohondan.com/admin/unlock/apiword/apihub/api-auth.php",
            "debug: 200 OK",
            "data/flashtools/debug/root权限获取成功.txt",
            "上传完成",
            "正在链接服务器...",
            "open xiaohondan.com/admin/unlock/apiword/apihub/api-auth.php",
            "GET /admin/unlock/apiword/apihub/api-auth.php HTTP/1.1",
            "mpl/1.0 (FakeFlashTool)",
            "Host: xiaohondan.com",
            "Connection: keep-alive",
            "User-Agent: FakeFlashTool/1.0",
            "Accept: */*",
            "Accept-Encoding: gzip, deflate",
            "neko login"
            "neko install api-host for xiaohondan.com",
            "neko login success",
            "ok debug: 200 OK",
            "all",
            "连接成功",
            "恭喜你解锁成功!",
        ]
        

        pause_points = [2, 7, 14, 19, 23, 27, 31, 35]
        
        for i, step in enumerate(steps):
            self.log_text.insert(tk.END, step + "\n")
            self.log_text.see(tk.END)
            self.root.update()
            
            if i in pause_points:
                time.sleep(2)
            else:
                time.sleep(0.5)
        


        
        errors = [""]
        self.log_text.insert(tk.END, random.choice(errors))
        self.log_text.insert(tk.END, "\n刷机完成！\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 显示提示
        messagebox.showinfo("刷机完成", "恭喜！刷机已完成！")
        
        # 重新启用按钮
        self.flash_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = FakeFlashTool(root)
        root.mainloop()
    except Exception as e:
        print(f"程序运行出错: {e}")
        input("按回车键退出...")
