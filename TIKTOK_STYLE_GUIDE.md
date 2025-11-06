# 🎬 TIKTOK STYLE UI - Swapping Panels Animation

## 🔥 PERSIS SEPERTI DI VIDEO!

Saya sudah bikin **UI persis seperti di TikTok** dengan panel yang swap kiri-kanan!

---

## ✨ FITUR UTAMA:

### 🎭 **Swapping Panels Animation**
- ✅ **Panel kiri ↔ kanan** dengan smooth animation
- ✅ **0.6 detik transition** (ease-in-out cubic)
- ✅ **Position absolute** dengan transform

### 🎨 **Design Elements**
- ✅ **Two-panel card** (800x500px)
- ✅ **Blue gradient welcome panel** (#6B9FFF → #5B8FEF)
- ✅ **White form panel** dengan rounded inputs
- ✅ **Rounded card** dengan shadow (25px radius)
- ✅ **Social login buttons** (Google, Facebook, GitHub, LinkedIn)
- ✅ **Gradient background** (light blue)

### 💫 **Interactive**
- ✅ **Hover effects** pada semua buttons
- ✅ **Focus states** pada inputs
- ✅ **Smooth transitions** pada semua elemen

---

## 📥 DOWNLOAD (2 files):

1. [**auth_ui_tiktok_style.py**](computer:///mnt/user-data/outputs/auth_ui_tiktok_style.py) - TikTok style auth UI
2. [**main_tiktok_style.py**](computer:///mnt/user-data/outputs/main_tiktok_style.py) - Launcher

---

## 🚀 CARA PAKAI:

### Step 1: Download & Copy
```
Download 2 file di atas → Copy ke folder project
```

### Step 2: Jalankan
```bash
python main_tiktok_style.py
```

### Step 3: Test Animation!
```
1. Klik button "Register" → Panel SWAP! 🔄
2. Klik button "Login" → Panel SWAP lagi! 🔄
```

---

## 🎬 ANIMASI YANG TERJADI:

### **Mode: Login (Default)**
```
┌────────────────────────────────────────────────┐
│                    │                            │
│  Hello, Welcome!   │        Login               │
│                    │                            │
│  Don't have        │    [Username     ]         │
│   an account?      │    [Password     ]         │
│                    │    Forgot Password?        │
│   [ Register ]     │    [   Login   ]           │
│                    │                            │
│                    │    G  f  🐙  in            │
│                    │                            │
└────────────────────────────────────────────────┘
    BLUE PANEL            WHITE PANEL
    (LEFT)                (RIGHT)
```

### **Klik "Register" → SWAP!**
```
         ⬅️ Panel geser kiri
         ➡️ Panel geser kanan

┌────────────────────────────────────────────────┐
│                            │                    │
│    Registration            │  Welcome Back!     │
│                            │                    │
│  [Username     ]           │  Already have      │
│  [Email        ]           │   an account?      │
│  [Password     ]           │                    │
│  [Role: user ▼ ]           │   [  Login  ]      │
│  [ Register ]              │                    │
│                            │                    │
│  G  f  🐙  in              │                    │
│                            │                    │
└────────────────────────────────────────────────┘
    WHITE PANEL                BLUE PANEL
    (LEFT)                     (RIGHT)
```

**PANEL BERTUKAR POSISI!** ✨

---

## 🎨 COLOR PALETTE:

```
Background:        #e0e7ff → #ccd5ff (gradient)
Card:              #ffffff (white)
Blue Gradient:     #6B9FFF → #5B8FEF
Input Background:  #f3f4f6 (light gray)
Text Primary:      #1f2937 (dark)
Text Secondary:    #6b7280 (gray)
Link Color:        #6B9FFF (blue)
Border:            #e5e7eb (light gray)
```

---

## 💻 TECHNICAL DETAILS:

### **Animation Code:**
```python
def swap_to_position(self, target_x):
    self.animation = QPropertyAnimation(self, b"pos")
    self.animation.setDuration(600)  # 0.6 seconds
    self.animation.setEasingCurve(QEasingCurve.InOutCubic)
    self.animation.start()
```

### **Panel States:**
- **Login Mode:** Welcome Left + Form Right
- **Register Mode:** Form Left + Welcome Right

### **Swap Logic:**
```python
# Login → Register
welcome_left.move(0 → 400)    # Geser kanan
login_panel.move(400 → 800)   # Keluar kanan
register_panel.move(0)        # Masuk dari kiri
welcome_right.move(400)       # Muncul kanan

# Register → Login (kebalikan)
```

---

## 📊 COMPARISON:

### **Beautiful Version (sebelumnya):**
- ❌ Slide tab biasa
- ❌ Stack widget
- ✅ Gradient theme

### **TikTok Version (BARU):**
- ✅ **Swapping panels** (persis TikTok)
- ✅ **Two-card design**
- ✅ **Smooth 0.6s animation**
- ✅ **Blue gradient welcome**
- ✅ **Social login buttons**
- 🔥 **LEBIH KEREN!**

---

## 🎯 TEST CHECKLIST:

1. ✅ **Initial state** - Login form di kanan, welcome di kiri
2. ✅ **Klik "Register"** - Panel swap smooth!
3. ✅ **Form register** - Username, email, password, role muncul
4. ✅ **Klik "Login"** - Panel swap kembali!
5. ✅ **Social buttons** - Google, Facebook, GitHub, LinkedIn
6. ✅ **Input fields** - Hover & focus states
7. ✅ **Forgot password** - Link clickable
8. ✅ **Register akun** - Buat user baru, otomatis balik ke login
9. ✅ **Login** - Masuk dengan user baru

---

## 🎉 HASIL:

**Progress:** 40% → **45%** 🚀

**Status:** 🔥 UI SEKARANG VIRAL-READY!

---

## 📸 SCREENSHOT TIME!

**PENTING:** Screenshot saat panel lagi swap ya! Biar keliatan animasinya! 🎬

1. Screenshot mode login
2. **Screenshot saat tengah animasi swap** (blur panel)
3. Screenshot mode register

---

## 💬 FEEDBACK:

Setelah test:
- 🔥 Apakah animasinya smooth?
- 🎨 Warnanya pas atau mau diganti?
- ⚡ Kecepatannya oke atau terlalu cepat/lambat?
- 💡 Ada yang mau ditambah?

---

**SELAMAT MENCOBA TIKTOK STYLE UI!** 🎬✨

Panel swap-nya bakal bikin WOW! 😍
