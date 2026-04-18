import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

def test_password_dialog():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 创建密码对话框
    pass_window = tk.Toplevel(root)
    pass_window.title("身份验证")
    pass_window.geometry("300x150")
    pass_window.resizable(False, False)
    pass_window.transient(root)
    pass_window.grab_set()
    
    # 居中显示
    pass_window.update_idletasks()
    x = (pass_window.winfo_screenwidth() // 2) - (300 // 2)
    y = (pass_window.winfo_screenheight() // 2) - (150 // 2)
    pass_window.geometry('+{}+{}'.format(x, y))
    
    attempts = 0
    
    ttk.Label(pass_window, text="请输入密码:", font=("Arial", 10)).pack(pady=10)
    
    password_var = tk.StringVar()
    password_entry = ttk.Entry(pass_window, textvariable=password_var, show="*")
    password_entry.pack(pady=5)
    password_entry.focus()
    
    def check_password():
        nonlocal attempts
        password = password_var.get()
        if password == "3815099625":
            messagebox.showinfo("登录成功", "密码正确，欢迎使用刷机软件！")
            pass_window.destroy()
            root.destroy()
        else:
            attempts += 1
            if attempts >= 3:
                # 创建自定义对话框
                error_window = tk.Toplevel(pass_window)
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
                    pass_window.destroy()
                    root.destroy()
                
                get_pwd_btn = ttk.Button(button_frame, text="获取密码", command=get_password)
                get_pwd_btn.pack(side=tk.LEFT, padx=10)
                
                # 退出按钮
                def exit_program():
                    error_window.destroy()
                    pass_window.destroy()
                    root.destroy()
                
                exit_btn = ttk.Button(button_frame, text="退出", command=exit_program)
                exit_btn.pack(side=tk.LEFT, padx=10)
                
                # 设置窗口为模态
                error_window.transient(pass_window)
                error_window.grab_set()
            else:
                messagebox.showerror("错误", f"密码错误！还剩{3-attempts}次尝试机会。")
                password_var.set("")
    
    submit_btn = ttk.Button(pass_window, text="确定", command=check_password)
    submit_btn.pack(pady=10)
    
    password_entry.bind("<Return>", lambda event: check_password())
    
    root.mainloop()

if __name__ == "__main__":
    test_password_dialog()