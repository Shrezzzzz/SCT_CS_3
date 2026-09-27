"""
PassGuard v2.4 Core — Password Strength Analysis Tool
A polished, cross-platform desktop cybersecurity utility built with CustomTkinter.
Works on Windows 10/11, Linux (Ubuntu/Kali), and macOS without code changes.
"""

import re
import string
import secrets
import customtkinter as ctk


# ──────────────────────────────────────────────
# Theme & Design Tokens
# ──────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Palette
BG_COLOR = "#F2F4F7"
CARD_COLOR = "#FFFFFF"
CARD_BORDER = "#E2E6EB"
TEXT_PRIMARY = "#1A1D21"
TEXT_SECONDARY = "#5F6B7A"
TEXT_MUTED = "#9CA3AF"

# Accent colours
BLUE_PRIMARY = "#2563EB"
BLUE_HOVER = "#1D4ED8"
BLUE_LIGHT = "#EFF6FF"
BLUE_BORDER = "#BFDBFE"
GREEN_PRIMARY = "#16A34A"
GREEN_HOVER = "#15803D"
GREEN_LIGHT = "#F0FDF4"
GREEN_BADGE_BG = "#DCFCE7"
GREEN_BADGE_TEXT = "#166534"
RED_DANGER = "#EF4444"

# Strength colours
STRENGTH_COLORS = {
    "Very Weak": "#EF4444",
    "Weak": "#F97316",
    "Moderate": "#EAB308",
    "Strong": "#22C55E",
    "Very Strong": "#16A34A",
}

SEGMENT_INACTIVE = "#E5E7EB"

FONT_FAMILY = "Inter"


# ──────────────────────────────────────────────
# Password analysis
# ──────────────────────────────────────────────

def evaluate_password(password: str) -> dict:
    """Evaluate password and return detailed analysis."""
    checks = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[" + re.escape(string.punctuation) + r"]", password)),
    }

    # Score out of 100
    score = 0
    if checks["length"]:
        score += 20
    if checks["uppercase"]:
        score += 15
    if checks["lowercase"]:
        score += 15
    if checks["digit"]:
        score += 15
    if checks["special"]:
        score += 15
    # Length bonuses
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10

    # Determine strength level (0-4 index)
    if score <= 20:
        label, level = "Very Weak", 0
    elif score <= 40:
        label, level = "Weak", 1
    elif score <= 60:
        label, level = "Moderate", 2
    elif score <= 80:
        label, level = "Strong", 3
    else:
        label, level = "Very Strong", 4

    colour = STRENGTH_COLORS[label]

    suggestions: list[str] = []
    if not checks["length"]:
        suggestions.append("Use at least 8 characters.")
    if not checks["uppercase"]:
        suggestions.append("Add uppercase letters (A-Z).")
    if not checks["lowercase"]:
        suggestions.append("Add lowercase letters (a-z).")
    if not checks["digit"]:
        suggestions.append("Include at least one number (0-9).")
    if not checks["special"]:
        suggestions.append("Include a special character (!@#$%…).")
    if len(password) < 12:
        suggestions.append("Consider making it 12+ characters.")

    return {
        "checks": checks,
        "score": score,
        "label": label,
        "level": level,
        "colour": colour,
        "suggestions": suggestions,
    }



# ──────────────────────────────────────────────
# Application UI
# ──────────────────────────────────────────────

class PassGuardApp(ctk.CTk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.title("PassGuard v2.4 Core")
        self.geometry("780x720")
        self.minsize(700, 680)
        self.configure(fg_color=BG_COLOR)

        self._password_visible = False
        self._build_ui()

    def _build_ui(self) -> None:
        # ── Scrollable main container ──
        main = ctk.CTkFrame(self, fg_color=BG_COLOR)
        main.pack(expand=True, fill="both")

        # Outer wrapper for centering
        wrapper = ctk.CTkFrame(main, fg_color="transparent", width=720)
        wrapper.pack(expand=True, fill="both", padx=30, pady=0)
        wrapper.grid_columnconfigure(0, weight=1)

        row = 0

        # ════════════════════════════════════════
        # TOP BAR
        # ════════════════════════════════════════
        topbar = ctk.CTkFrame(wrapper, fg_color="transparent", height=40)
        topbar.grid(row=row, column=0, sticky="ew", pady=(18, 0))
        topbar.grid_columnconfigure(1, weight=1)

        # Left: icon + title
        left_bar = ctk.CTkFrame(topbar, fg_color="transparent")
        left_bar.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            left_bar, text="🛡", font=(FONT_FAMILY, 18),
        ).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            left_bar, text="PassGuard", font=(FONT_FAMILY, 15, "bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")
        ctk.CTkLabel(
            left_bar, text="v2.4 Core", font=(FONT_FAMILY, 12),
            text_color=TEXT_MUTED,
        ).pack(side="left", padx=(6, 0))

        # Right: badge
        badge = ctk.CTkFrame(topbar, fg_color=GREEN_BADGE_BG, corner_radius=12, height=28)
        badge.grid(row=0, column=2, sticky="e")
        ctk.CTkLabel(
            badge, text="●  Offline Security Checker  🔒",
            font=(FONT_FAMILY, 11, "bold"), text_color=GREEN_BADGE_TEXT,
        ).pack(padx=12, pady=4)

        row += 1

        # ════════════════════════════════════════
        # MAIN CARD
        # ════════════════════════════════════════
        card = ctk.CTkFrame(
            wrapper, fg_color=CARD_COLOR, corner_radius=14,
            border_width=1, border_color=CARD_BORDER,
        )
        card.grid(row=row, column=0, sticky="ew", pady=(14, 0))
        card.grid_columnconfigure(0, weight=1)

        pad_x = 28
        c_row = 0

        # ── Header inside card ──
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.grid(row=c_row, column=0, sticky="ew", padx=pad_x, pady=(24, 0))
        header.grid_columnconfigure(1, weight=1)

        # Shield icon
        shield_frame = ctk.CTkFrame(header, fg_color=BLUE_PRIMARY, corner_radius=12, width=52, height=52)
        shield_frame.grid(row=0, column=0, rowspan=2, sticky="w")
        shield_frame.grid_propagate(False)
        ctk.CTkLabel(
            shield_frame, text="🛡", font=(FONT_FAMILY, 22),
            text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            header, text="PassGuard", font=(FONT_FAMILY, 22, "bold"),
            text_color=TEXT_PRIMARY,
        ).grid(row=0, column=1, sticky="sw", padx=(14, 0))
        ctk.CTkLabel(
            header, text="Password Strength Analysis Tool",
            font=(FONT_FAMILY, 13), text_color=TEXT_SECONDARY,
        ).grid(row=1, column=1, sticky="nw", padx=(14, 0))

        # Local Analysis badge
        local_badge = ctk.CTkFrame(header, fg_color="#F8FAFC", corner_radius=8,
                                    border_width=1, border_color=CARD_BORDER)
        local_badge.grid(row=0, column=2, rowspan=2, sticky="e")
        ctk.CTkLabel(
            local_badge, text="🛡  Local Analysis",
            font=(FONT_FAMILY, 12), text_color=TEXT_SECONDARY,
        ).pack(padx=12, pady=6)

        c_row += 1

        # ── Password input section ──
        input_header = ctk.CTkFrame(card, fg_color="transparent")
        input_header.grid(row=c_row, column=0, sticky="ew", padx=pad_x, pady=(22, 0))
        input_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            input_header, text="Enter Password",
            font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        self.char_count_label = ctk.CTkLabel(
            input_header, text="0 characters",
            font=(FONT_FAMILY, 12), text_color=TEXT_MUTED,
        )
        self.char_count_label.grid(row=0, column=1, sticky="e")

        c_row += 1

        # Entry row
        entry_frame = ctk.CTkFrame(card, fg_color="transparent")
        entry_frame.grid(row=c_row, column=0, sticky="ew", padx=pad_x, pady=(8, 0))
        entry_frame.grid_columnconfigure(0, weight=1)

        self.password_var = ctk.StringVar()
        self.password_var.trace_add("write", self._on_password_change)

        self.entry = ctk.CTkEntry(
            entry_frame, textvariable=self.password_var,
            show="●", height=46, corner_radius=10,
            font=(FONT_FAMILY, 14),
            placeholder_text="  🔗  Enter your password…",
            placeholder_text_color=TEXT_MUTED,
            border_width=1, border_color=CARD_BORDER,
            fg_color="#F9FAFB",
        )
        self.entry.grid(row=0, column=0, sticky="ew")

        btn_group = ctk.CTkFrame(entry_frame, fg_color="transparent")
        btn_group.grid(row=0, column=1, padx=(6, 0))

        self.toggle_btn = ctk.CTkButton(
            btn_group, text="👁", width=42, height=42,
            corner_radius=8, fg_color="#F3F4F6",
            hover_color="#E5E7EB", text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, 16), command=self._toggle_visibility,
        )
        self.toggle_btn.pack(side="left", padx=(0, 4))

        self.copy_btn = ctk.CTkButton(
            btn_group, text="📋", width=42, height=42,
            corner_radius=8, fg_color="#F3F4F6",
            hover_color="#E5E7EB", text_color=TEXT_SECONDARY,
            font=(FONT_FAMILY, 16), command=self._copy_password,
        )
        self.copy_btn.pack(side="left")

        c_row += 1

        # ════════════════════════════════════════
        # STRENGTH ANALYSIS CARD
        # ════════════════════════════════════════
        strength_card = ctk.CTkFrame(
            card, fg_color="#FAFBFC", corner_radius=10,
            border_width=1, border_color=CARD_BORDER,
        )
        strength_card.grid(row=c_row, column=0, sticky="ew", padx=pad_x, pady=(18, 0))
        strength_card.grid_columnconfigure(0, weight=1)

        # Strength header
        s_header = ctk.CTkFrame(strength_card, fg_color="transparent")
        s_header.grid(row=0, column=0, sticky="ew", padx=18, pady=(14, 0))
        s_header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            s_header, text="🔄  Strength Analysis",
            font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_PRIMARY,
        ).grid(row=0, column=0, sticky="w")

        self.strength_pct_label = ctk.CTkLabel(
            s_header, text="0% • --",
            font=(FONT_FAMILY, 13, "bold"), text_color=TEXT_MUTED,
        )
        self.strength_pct_label.grid(row=0, column=1, sticky="e")

        # Segmented progress bar
        seg_frame = ctk.CTkFrame(strength_card, fg_color="transparent")
        seg_frame.grid(row=1, column=0, sticky="ew", padx=18, pady=(10, 0))
        for i in range(5):
            seg_frame.grid_columnconfigure(i, weight=1)

        self.segments: list[ctk.CTkFrame] = []
        for i in range(5):
            seg = ctk.CTkFrame(
                seg_frame, height=10, corner_radius=5,
                fg_color=SEGMENT_INACTIVE,
            )
            px_l = 0 if i == 0 else 3
            px_r = 0 if i == 4 else 3
            seg.grid(row=0, column=i, sticky="ew", padx=(px_l, px_r))
            self.segments.append(seg)

        # Strength level labels
        labels_frame = ctk.CTkFrame(strength_card, fg_color="transparent")
        labels_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(8, 14))
        for i in range(5):
            labels_frame.grid_columnconfigure(i, weight=1)

        level_names = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
        self.level_labels: list[ctk.CTkLabel] = []
        self.level_frames: list[ctk.CTkFrame] = []
        for i, name in enumerate(level_names):
            frame = ctk.CTkFrame(labels_frame, fg_color="transparent", corner_radius=6)
            px_l = 0 if i == 0 else 3
            px_r = 0 if i == 4 else 3
            frame.grid(row=0, column=i, sticky="ew", padx=(px_l, px_r))

            lbl = ctk.CTkLabel(
                frame, text=name, font=(FONT_FAMILY, 11),
                text_color=TEXT_MUTED,
            )
            lbl.pack(pady=4)
            self.level_labels.append(lbl)
            self.level_frames.append(frame)

        c_row += 1

        # ════════════════════════════════════════
        # SECURITY VERIFICATION CHECKLIST
        # ════════════════════════════════════════
        ctk.CTkLabel(
            card, text="Security Verification Checklist",
            font=(FONT_FAMILY, 14, "bold"), text_color=TEXT_PRIMARY,
            anchor="w",
        ).grid(row=c_row, column=0, sticky="w", padx=pad_x, pady=(20, 8))

        c_row += 1

        checklist_grid = ctk.CTkFrame(card, fg_color="transparent")
        checklist_grid.grid(row=c_row, column=0, sticky="ew", padx=pad_x)
        checklist_grid.grid_columnconfigure((0, 1), weight=1)

        check_items = [
            ("length", "At least 8 characters", 0, 0),
            ("uppercase", "Contains uppercase letters", 0, 1),
            ("lowercase", "Contains lowercase letters", 1, 0),
            ("digit", "Contains numbers", 1, 1),
            ("special", "Contains special characters (!@#$%^&*)", 2, 0),
        ]

        self.check_icons: dict[str, ctk.CTkLabel] = {}
        self.check_texts: dict[str, ctk.CTkLabel] = {}
        self.check_cards: dict[str, ctk.CTkFrame] = {}

        for key, desc, r, c in check_items:
            colspan = 2 if key == "special" else 1
            item_card = ctk.CTkFrame(
                checklist_grid, fg_color="#F9FAFB", corner_radius=8,
                border_width=1, border_color=CARD_BORDER, height=44,
            )
            px_l = 0 if c == 0 else 4
            px_r = 0 if c == 1 or colspan == 2 else 4
            item_card.grid(row=r, column=c, columnspan=colspan,
                           sticky="ew", padx=(px_l, px_r), pady=4)
            item_card.grid_propagate(False)
            item_card.grid_columnconfigure(1, weight=1)

            icon_lbl = ctk.CTkLabel(
                item_card, text="○", font=(FONT_FAMILY, 16),
                text_color=TEXT_MUTED, width=30,
            )
            icon_lbl.grid(row=0, column=0, padx=(12, 0), pady=10, sticky="w")

            text_lbl = ctk.CTkLabel(
                item_card, text=desc, font=(FONT_FAMILY, 12),
                text_color=TEXT_SECONDARY, anchor="w",
            )
            text_lbl.grid(row=0, column=1, padx=(4, 12), pady=10, sticky="w")

            self.check_icons[key] = icon_lbl
            self.check_texts[key] = text_lbl
            self.check_cards[key] = item_card


        c_row += 1

        # ════════════════════════════════════════
        # ACTION BUTTONS
        # ════════════════════════════════════════
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=c_row, column=0, sticky="ew", padx=pad_x, pady=(20, 24))
        btn_row.grid_columnconfigure(0, weight=1)

        self.clear_btn = ctk.CTkButton(
            btn_row, text="Clear", height=44, corner_radius=10, width=100,
            font=(FONT_FAMILY, 14, "bold"),
            fg_color="#FFFFFF", hover_color="#F3F4F6",
            text_color=RED_DANGER,
            border_width=1, border_color=CARD_BORDER,
            command=self._reset,
        )
        self.clear_btn.grid(row=0, column=0, sticky="e")

        row += 1

        # ════════════════════════════════════════
        # FOOTER
        # ════════════════════════════════════════
        footer = ctk.CTkFrame(wrapper, fg_color="transparent")
        footer.grid(row=row, column=0, sticky="ew", pady=(12, 16))
        footer.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            footer, text="●  Offline Password Analysis  •  No Data Stored Locally",
            font=(FONT_FAMILY, 11), text_color=GREEN_PRIMARY, anchor="w",
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            footer, text="Zero Network Telemetry",
            font=("Courier", 11), text_color=TEXT_MUTED, anchor="e",
        ).grid(row=0, column=1, sticky="e")

    # ── Callbacks ─────────────────────────────

    def _on_password_change(self, *_args) -> None:
        """Live analysis as the user types."""
        pw = self.password_var.get()
        length = len(pw)
        self.char_count_label.configure(
            text=f"{length} character{'s' if length != 1 else ''}"
        )
        self._analyse()

    def _toggle_visibility(self) -> None:
        self._password_visible = not self._password_visible
        self.entry.configure(show="" if self._password_visible else "●")
        self.toggle_btn.configure(text="🙈" if self._password_visible else "👁")

    def _copy_password(self) -> None:
        pw = self.password_var.get()
        if pw:
            self.clipboard_clear()
            self.clipboard_append(pw)
            # Brief visual feedback
            original = self.copy_btn.cget("text")
            self.copy_btn.configure(text="✅")
            self.after(1200, lambda: self.copy_btn.configure(text=original))

    def _analyse(self) -> None:
        password = self.password_var.get()

        if not password:
            self._reset_display()
            return

        result = evaluate_password(password)

        # ── Strength percentage label ──
        self.strength_pct_label.configure(
            text=f"{result['score']}%  •  {result['label']}",
            text_color=result["colour"],
        )

        # ── Segmented progress bar ──
        for i in range(5):
            if i <= result["level"]:
                self.segments[i].configure(fg_color=result["colour"])
            else:
                self.segments[i].configure(fg_color=SEGMENT_INACTIVE)

        # ── Level labels ──
        for i in range(5):
            if i == result["level"]:
                self.level_frames[i].configure(fg_color=result["colour"])
                self.level_labels[i].configure(text_color="#FFFFFF")
            else:
                self.level_frames[i].configure(fg_color="transparent")
                self.level_labels[i].configure(text_color=TEXT_MUTED)

        # ── Checklist ──
        for key, passed in result["checks"].items():
            if passed:
                self.check_icons[key].configure(text="✅", text_color=GREEN_PRIMARY)
                self.check_texts[key].configure(text_color=TEXT_PRIMARY)
                self.check_cards[key].configure(fg_color="#F0FDF4", border_color="#BBF7D0")
            else:
                self.check_icons[key].configure(text="❌", text_color=RED_DANGER)
                self.check_texts[key].configure(text_color=TEXT_SECONDARY)
                self.check_cards[key].configure(fg_color="#FEF2F2", border_color="#FECACA")


    def _reset(self) -> None:
        self.password_var.set("")
        self.entry.configure(show="●")
        self._password_visible = False
        self.toggle_btn.configure(text="👁")
        self.char_count_label.configure(text="0 characters")
        self._reset_display()
        self.entry.focus_set()

    def _reset_display(self) -> None:
        self.strength_pct_label.configure(text="0% • --", text_color=TEXT_MUTED)

        for seg in self.segments:
            seg.configure(fg_color=SEGMENT_INACTIVE)

        for i in range(5):
            self.level_frames[i].configure(fg_color="transparent")
            self.level_labels[i].configure(text_color=TEXT_MUTED)

        for key in self.check_icons:
            self.check_icons[key].configure(text="○", text_color=TEXT_MUTED)
            self.check_texts[key].configure(text_color=TEXT_SECONDARY)
            self.check_cards[key].configure(fg_color="#F9FAFB", border_color=CARD_BORDER)




# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    app = PassGuardApp()
    app.mainloop()
