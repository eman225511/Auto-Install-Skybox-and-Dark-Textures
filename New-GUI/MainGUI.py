import os
import shutil
import glob
import ctypes
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

def set_console_color():
    # Set console color to light cyan on black (Windows only)
    os.system('color 0B')

def pause():
    input("Press Enter to continue...")

def make_readonly(filepath):
    try:
        os.chmod(filepath, 0o444)
    except Exception:
        # Fallback for Windows
        FILE_ATTRIBUTE_READONLY = 0x01
        ctypes.windll.kernel32.SetFileAttributesW(str(filepath), FILE_ATTRIBUTE_READONLY)

def install_skybox(chosen_skybox):
    print(f"[DEBUG] Installing skybox: {chosen_skybox}")
    install_assets()
    localappdata = os.environ.get('LOCALAPPDATA')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rbx_versions = os.path.join(localappdata, 'Roblox', 'Versions')
    skybox_textures = os.path.join(script_dir, 'skybox')
    chosen_skybox_path = os.path.join(skybox_textures, chosen_skybox)
    for version in glob.glob(os.path.join(rbx_versions, '*')):
        sky_path = os.path.join(version, 'PlatformContent', 'pc', 'textures', 'sky')
        if os.path.exists(sky_path):
            print(f"[DEBUG] Replacing skybox in: {sky_path}")
            # Only remove .tex files that start with 'sky'
            for f in glob.glob(os.path.join(sky_path, 'sky*.tex')):
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"[ERROR] Could not remove {f}: {e}")
            for tex_file in glob.glob(os.path.join(chosen_skybox_path, '*.tex')):
                print(f"[DEBUG] Copying {tex_file} to {sky_path}")
                shutil.copy2(tex_file, sky_path)

def install_assets():
    print("[DEBUG] Installing assets...")
    localappdata = os.environ.get('LOCALAPPDATA')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rbx_storage = os.path.join(localappdata, 'Roblox', 'rbx-storage')
    assets = os.path.join(script_dir, 'assets')

    asset_files = [
        ('a564ec8aeef3614e788d02f0090089d8', 'a5'),
        ('7328622d2d509b95dd4dd2c721d1ca8b', '73'),
        ('a50f6563c50ca4d5dcb255ee5cfab097', 'a5'),
        ('6c94b9385e52d221f0538aadaceead2d', '6c'),
        ('9244e00ff9fd6cee0bb40a262bb35d31', '92'),
        ('78cb2e93aee0cdbd79b15a866bc93a54', '78'),
    ]

    for folder in ['a5', '73', '6c', '92', '78']:
        os.makedirs(os.path.join(rbx_storage, folder), exist_ok=True)

    for filename, folder in asset_files:
        src = os.path.join(assets, filename)
        dst = os.path.join(rbx_storage, folder, filename)
        try:
            # Remove read-only if file exists
            if os.path.exists(dst):
                try:
                    os.chmod(dst, 0o666)
                except Exception:
                    FILE_ATTRIBUTE_NORMAL = 0x80
                    ctypes.windll.kernel32.SetFileAttributesW(str(dst), FILE_ATTRIBUTE_NORMAL)
            print(f"[DEBUG] Copying asset {src} to {dst}")
            shutil.copy2(src, dst)
            make_readonly(dst)
        except Exception as e:
            print(f"[ERROR] Could not copy asset {src} to {dst}: {e}")

def install_dark_textures():
    print("[DEBUG] Installing dark textures...")
    localappdata = os.environ.get('LOCALAPPDATA')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rbx_versions = os.path.join(localappdata, 'Roblox', 'Versions')
    dark_textures = os.path.join(script_dir, 'dark')
    if not os.path.exists(rbx_versions):
        print("[ERROR] Roblox versions folder not found!")
        messagebox.showerror("Error", "Roblox versions folder not found!")
        return
    if not os.path.exists(dark_textures):
        print("[ERROR] Dark textures folder not found!")
        messagebox.showerror("Error", "Dark textures folder not found!")
        return
    for version in glob.glob(os.path.join(rbx_versions, '*')):
        textures_path = os.path.join(version, 'PlatformContent', 'pc', 'textures')
        if os.path.exists(textures_path):
            print(f"[DEBUG] Replacing textures in: {textures_path}")
            for f in glob.glob(os.path.join(textures_path, '*')):
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"[ERROR] Could not remove {f}: {e}")
            for item in os.listdir(dark_textures):
                s = os.path.join(dark_textures, item)
                d = os.path.join(textures_path, item)
                if os.path.isdir(s):
                    print(f"[DEBUG] Copying directory {s} to {d}")
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    print(f"[DEBUG] Copying file {s} to {d}")
                    shutil.copy2(s, d)

def restore_skybox():
    print("[DEBUG] Restoring default skybox from stock_sky...")
    localappdata = os.environ.get('LOCALAPPDATA')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rbx_versions = os.path.join(localappdata, 'Roblox', 'Versions')
    stock_sky = os.path.join(script_dir, 'stock_sky')
    if not os.path.exists(stock_sky):
        print("[ERROR] stock_sky folder not found!")
        messagebox.showerror("Error", "stock_sky folder not found!")
        return
    for version in glob.glob(os.path.join(rbx_versions, '*')):
        sky_path = os.path.join(version, 'PlatformContent', 'pc', 'textures', 'sky')
        if os.path.exists(sky_path):
            print(f"[DEBUG] Restoring skybox in: {sky_path}")
            # Only remove .tex files that start with 'sky'
            for f in glob.glob(os.path.join(sky_path, 'sky*.tex')):
                try:
                    os.remove(f)
                except Exception as e:
                    print(f"[ERROR] Could not remove {f}: {e}")
            for tex_file in glob.glob(os.path.join(stock_sky, '*.tex')):
                print(f"[DEBUG] Copying {tex_file} to {sky_path}")
                shutil.copy2(tex_file, sky_path)
    messagebox.showinfo("Restored", "Default skybox restored from stock_sky.")

def full_restore():
    print("[DEBUG] Performing FULL RESTORE: Replacing all textures with stock_textures...")
    localappdata = os.environ.get('LOCALAPPDATA')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rbx_versions = os.path.join(localappdata, 'Roblox', 'Versions')
    stock_textures = os.path.join(script_dir, 'stock_textures')
    if not os.path.exists(stock_textures):
        print("[ERROR] stock_textures folder not found!")
        messagebox.showerror("Error", "stock_textures folder not found!")
        return
    replaced = 0
    for version in glob.glob(os.path.join(rbx_versions, '*')):
        textures_path = os.path.join(version, 'PlatformContent', 'pc', 'textures')
        if os.path.exists(textures_path):
            print(f"[DEBUG] Replacing textures in: {textures_path}")
            # Remove all current textures
            for f in glob.glob(os.path.join(textures_path, '*')):
                try:
                    if os.path.isdir(f):
                        shutil.rmtree(f)
                    else:
                        os.remove(f)
                except Exception as e:
                    print(f"[ERROR] Could not remove {f}: {e}")
            # Copy all from stock_textures
            for item in os.listdir(stock_textures):
                s = os.path.join(stock_textures, item)
                d = os.path.join(textures_path, item)
                try:
                    if os.path.isdir(s):
                        shutil.copytree(s, d, dirs_exist_ok=True)
                    else:
                        shutil.copy2(s, d)
                except Exception as e:
                    print(f"[ERROR] Could not copy {s} to {d}: {e}")
            replaced += 1
    messagebox.showinfo("Full Restore", f"Replaced textures in {replaced} Roblox version(s) with stock_textures.")

def main_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    skybox_textures = os.path.join(script_dir, 'skybox')
    skybox_folders = [f for f in os.listdir(skybox_textures) if os.path.isdir(os.path.join(skybox_textures, f))]
    if not skybox_folders:
        messagebox.showerror("Error", "No skybox textures found.")
        return

    root = ctk.CTk()
    root.title("Roblox Skybox Installer")
    root.geometry("400x640")
    root.resizable(False, False)

    # Main container to center everything
    container = ctk.CTkFrame(root, fg_color="transparent")
    container.pack(expand=True, fill="both")

    # Title
    ctk.CTkLabel(
        container,
        text="Roblox Skybox Installer",
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=(18, 10))

    # Skybox selection frame
    select_frame = ctk.CTkFrame(container, fg_color="transparent")
    select_frame.pack(pady=(0, 8), padx=32, anchor="center")

    ctk.CTkLabel(
        select_frame,
        text="Choose a Skybox Texture:",
        font=ctk.CTkFont(size=15, weight="bold"),
        anchor="center",
        justify="center"
    ).pack(anchor="center", pady=(0, 6))

    selected = ctk.StringVar(value=skybox_folders[0])
    dropdown = ctk.CTkComboBox(
        select_frame,
        variable=selected,
        values=skybox_folders,
        state="readonly",
        width=240,
        justify="center"
    )
    dropdown.pack(pady=(0, 10), anchor="center")

    # Preview frame
    preview_frame = ctk.CTkFrame(container, fg_color="transparent", corner_radius=12)
    preview_frame.pack(pady=(0, 18), padx=32, anchor="center")

    img_label = ctk.CTkLabel(
        preview_frame,
        text="No preview available",
        fg_color="transparent",
        text_color="#888",
        anchor="center",
        corner_radius=8
    )
    img_label.pack(padx=8, pady=8)

    def update_preview(*args):
        try:
            chosen_skybox_path = os.path.join(skybox_textures, selected.get())
            png_files = [f for f in os.listdir(chosen_skybox_path) if f.lower().endswith('.png')]
            if not png_files:
                img_label.configure(text="No preview available")
                img_label.image = None
                return
            img_path = os.path.join(chosen_skybox_path, png_files[0])
            img = Image.open(img_path).convert("RGBA")
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(220, 220))  # <-- Set desired size here
            img_label.configure(image=ctk_img, text="")
            img_label.image = ctk_img
        except Exception as e:
            img_label.configure(text="No preview available")
            img_label.image = None
            print(f"[ERROR] Could not update preview: {e}")

    selected.trace_add("write", update_preview)
    update_preview()

    def on_apply():
        install_skybox(selected.get())
        messagebox.showinfo("Done", f"Skybox '{selected.get()}' installed.")

    # Button frame
    btn_frame = ctk.CTkFrame(container, fg_color="#222", corner_radius=12)
    btn_frame.pack(pady=10, fill="x", padx=64)

    btn_style = {"width": 220, "height": 36, "font": ctk.CTkFont(size=14, weight="bold")}

    ctk.CTkButton(btn_frame, text="Apply Skybox", command=on_apply, **btn_style).pack(pady=(16, 8))
    ctk.CTkButton(btn_frame, text="Apply Dark Textures", command=lambda: [install_dark_textures(), messagebox.showinfo("Done", "Dark textures installed.")], **btn_style).pack(pady=8)
    ctk.CTkButton(btn_frame, text="Restore Sky", command=restore_skybox, **btn_style).pack(pady=8)
    ctk.CTkButton(btn_frame, text="Full Restore", command=lambda: [full_restore(), messagebox.showinfo("Done", "Full restore completed.")], **btn_style).pack(pady=(8, 16))

    root.mainloop()

if __name__ == "__main__":
    set_console_color()
    main_gui()

