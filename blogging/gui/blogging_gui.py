import tkinter as tk
from tkinter import messagebox, scrolledtext
from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.illegal_access_exception import IllegalAccessException

class BloggingGUI:
    def __init__(self):
        self.controller = Controller()
        self.win = tk.Tk()
        self.win.title("Blogging System")
        self.win.geometry("820x620")
        self.win.configure(bg="#f4f4f4")

        # create main containers
        self.top_frame = tk.Frame(self.win, bg="#f4f4f4")
        self.top_frame.pack(fill="x", pady=10)

        self.middle_frame = tk.Frame(self.win, bg="#f4f4f4")
        self.middle_frame.pack(fill="both", expand=True)

        self.bottom_frame = tk.Frame(self.win, bg="#f4f4f4")
        self.bottom_frame.pack(fill="x", pady=10)

        # status label
        self.status_label = tk.Label(self.bottom_frame, text="Not logged in", fg="red", bg="#f4f4f4")
        self.status_label.pack()

        # call UI setup
        self.make_login_box()
        self.make_blog_panel()

    # ---------------- LOGIN PANEL ----------------
    def make_login_box(self):
        login_box = tk.LabelFrame(self.top_frame, text="Login", padx=10, pady=10, bg="#f4f4f4")
        login_box.pack(pady=5)

        tk.Label(login_box, text="Username:", bg="#f4f4f4").grid(row=0, column=0)
        tk.Label(login_box, text="Password:", bg="#f4f4f4").grid(row=1, column=0)

        self.user_entry = tk.Entry(login_box, width=20)
        self.pass_entry = tk.Entry(login_box, width=20, show="*")
        self.user_entry.grid(row=0, column=1, padx=5)
        self.pass_entry.grid(row=1, column=1, padx=5)

        tk.Button(login_box, text="Login", command=self.do_login, width=10).grid(row=0, column=2, padx=5)
        tk.Button(login_box, text="Logout", command=self.do_logout, width=10).grid(row=1, column=2, padx=5)

    # ---------------- BLOG PANEL ----------------
    def make_blog_panel(self):
        left_frame = tk.LabelFrame(self.middle_frame, text="Blogs", bg="#f4f4f4", padx=10, pady=10)
        left_frame.pack(side="left", fill="y", padx=10, pady=5)

        right_frame = tk.LabelFrame(self.middle_frame, text="Posts", bg="#f4f4f4", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

        # BLOG LIST
        tk.Label(left_frame, text="Blog List:", bg="#f4f4f4").pack()
        self.blog_list = tk.Listbox(left_frame, width=30, height=20)
        self.blog_list.pack(pady=5)

        tk.Button(left_frame, text="Refresh", command=self.load_blogs).pack(pady=2)
        tk.Button(left_frame, text="Select Blog", command=self.select_blog).pack(pady=2)

        # create blog
        tk.Label(left_frame, text="Create Blog:", bg="#f4f4f4").pack(pady=(10, 2))
        self.cb_id = tk.Entry(left_frame, width=20)
        self.cb_title = tk.Entry(left_frame, width=20)
        self.cb_name = tk.Entry(left_frame, width=20)
        self.cb_email = tk.Entry(left_frame, width=20)
        tk.Label(left_frame, text="ID:", bg="#f4f4f4").pack()
        self.cb_id.pack()
        tk.Label(left_frame, text="Title:", bg="#f4f4f4").pack()
        self.cb_title.pack()
        tk.Label(left_frame, text="User:", bg="#f4f4f4").pack()
        self.cb_name.pack()
        tk.Label(left_frame, text="Email:", bg="#f4f4f4").pack()
        self.cb_email.pack()

        tk.Button(left_frame, text="Create", command=self.create_blog).pack(pady=4)
        tk.Button(left_frame, text="Delete", command=self.delete_blog).pack()

        # ---------------- POSTS ----------------
        tk.Label(right_frame, text="Posts for Current Blog:", bg="#f4f4f4").pack()
        self.post_list = tk.Listbox(right_frame, width=50, height=12)
        self.post_list.pack(pady=5)

        # post creation area
        tk.Label(right_frame, text="Create Post:", bg="#f4f4f4").pack()
        self.post_title = tk.Entry(right_frame, width=40)
        self.post_title.pack(pady=2)
        self.post_text = scrolledtext.ScrolledText(right_frame, width=40, height=6)
        self.post_text.pack(pady=2)

        tk.Button(right_frame, text="Add Post", command=self.add_post).pack(pady=3)
        tk.Button(right_frame, text="Delete Selected Post", command=self.delete_post).pack(pady=3)

    # ------------------- LOGIN LOGIC --------------------
    def do_login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()
        try:
            ok = self.controller.login(u, p)
            if ok:
                self.status_label.config(text=f"Logged in as {u}", fg="green")
        except InvalidLoginException:
            messagebox.showerror("Login", "Invalid username or password.")
        except IllegalOperationException:
            messagebox.showerror("Login", "Login failed (operation issue).")

    def do_logout(self):
        try:
            self.controller.logout()
            self.status_label.config(text="Not logged in", fg="red")
        except InvalidLogoutException:
            messagebox.showerror("Logout", "Cannot logout (not logged in).")

    # ------------------- BLOG LOGIC ---------------------
    def load_blogs(self):
        self.blog_list.delete(0, tk.END)
        try:
            blogs = self.controller.list_blogs()
            for b in blogs:
                self.blog_list.insert(tk.END, f"{b.id} | {b.title}")
        except IllegalAccessException:
            messagebox.showerror("Error", "You must log in first.")
        except Exception:
            messagebox.showerror("Error", "Failed to load blogs.")

    def select_blog(self):
        try:
            idx = self.blog_list.curselection()
            if not idx:
                messagebox.showwarning("Blog", "Select a blog first.")
                return
            row = self.blog_list.get(idx[0])
            bid = int(row.split("|")[0].strip())
            self.controller.set_current_blog(bid)
            self.load_posts()
        except IllegalOperationException:
            messagebox.showerror("Blog", "Invalid blog selection.")
        except Exception:
            messagebox.showerror("Blog", "Could not select blog.")

    def create_blog(self):
        try:
            bid = int(self.cb_id.get().strip())
            t = self.cb_title.get().strip()
            n = self.cb_name.get().strip()
            e = self.cb_email.get().strip()
            self.controller.create_blog(bid, t, n, e)
            self.load_blogs()
        except Exception as ex:
            messagebox.showerror("Create Blog", f"Error: {ex}")

    def delete_blog(self):
        try:
            idx = self.blog_list.curselection()
            if not idx:
                messagebox.showwarning("Blog", "Select a blog first.")
                return
            row = self.blog_list.get(idx[0])
            bid = int(row.split("|")[0].strip())
            self.controller.delete_blog(bid)
            self.load_blogs()
            self.post_list.delete(0, tk.END)
        except IllegalOperationException:
            messagebox.showerror("Delete Blog", "Cannot delete this blog.")
        except IllegalAccessException:
            messagebox.showerror("Delete Blog", "You must log in first.")
        except Exception as ex:
            messagebox.showerror("Delete Blog", f"Error: {ex}")

    # ------------------- POST LOGIC --------------------
    def load_posts(self):
        self.post_list.delete(0, tk.END)
        try:
            posts = self.controller.list_posts()
            for p in posts:
                self.post_list.insert(tk.END, f"{p.code}: {p.title}")
        except NoCurrentBlogException:
            messagebox.showwarning("Posts", "No blog selected.")
        except Exception:
            messagebox.showerror("Posts", "Could not load posts.")

    def add_post(self):
        try:
            t = self.post_title.get().strip()
            txt = self.post_text.get("1.0", tk.END).strip()
            if t == "" or txt == "":
                messagebox.showwarning("Post", "Title and text cannot be empty.")
                return
            self.controller.create_post(t, txt)
            self.post_title.delete(0, tk.END)
            self.post_text.delete("1.0", tk.END)
            self.load_posts()
        except Exception as ex:
            messagebox.showerror("Post", f"Error: {ex}")

    def delete_post(self):
        try:
            idx = self.post_list.curselection()
            if not idx:
                messagebox.showwarning("Post", "Select a post first.")
                return
            row = self.post_list.get(idx[0])
            code = int(row.split(":")[0])
            self.controller.delete_post(code)
            self.load_posts()
        except IllegalOperationException:
            messagebox.showerror("Delete Post", "Cannot delete this post.")
        except Exception as ex:
            messagebox.showerror("Delete Post", f"Error: {ex}")

    # ------------------- RUN --------------------
    def run(self):
        self.win.mainloop()


if __name__ == "__main__":
    gui = BloggingGUI()
    gui.run()
