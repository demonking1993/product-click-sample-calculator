import math
import sys
import tkinter as tk
from statistics import NormalDist
from tkinter import messagebox


APP_NAME = "测款神器"
APP_VERSION = "1.0"
FONT_UI = "PingFang SC" if sys.platform == "darwin" else "Microsoft YaHei UI"
CURSOR_HAND = "pointinghand" if sys.platform == "darwin" else "hand2"

COLORS = {
    "bg": "#F4F6FB",
    "navy": "#17233C",
    "muted": "#68738A",
    "line": "#E4E8F1",
    "white": "#FFFFFF",
    "primary": "#5B5CE2",
    "primary_dark": "#4647BE",
    "primary_light": "#EEF0FF",
    "green": "#12A675",
    "green_light": "#E9F8F2",
    "orange": "#F59E42",
    "orange_light": "#FFF4E8",
    "red": "#D94E64",
}


def calculate_sample_size(confidence_percent: float, relative_error_percent: float, p1_percent: float):
    """Return the normal-approximation sample size and related display values."""
    if not 0 < confidence_percent < 100:
        raise ValueError("观测可信度 a 必须大于 0% 且小于 100%")
    if not 0 < relative_error_percent < 100:
        raise ValueError("上下浮动 r 必须大于 0% 且小于 100%")
    if not 0 < p1_percent < 100:
        raise ValueError("真实购买率 p1 必须大于 0% 且小于 100%")

    a = confidence_percent / 100
    r = relative_error_percent / 100
    p1 = p1_percent / 100
    z = NormalDist().inv_cdf((1 + a) / 2)
    raw_m = (z * z * (1 - p1)) / (r * r * p1)
    m = math.ceil(raw_m)

    low_rate = max(0.0, p1 * (1 - r))
    high_rate = min(1.0, p1 * (1 + r))
    expected_buyers = m * p1
    min_buyers = math.ceil(m * low_rate)
    max_buyers = math.floor(m * high_rate)

    return {
        "m": m,
        "raw_m": raw_m,
        "z": z,
        "low_rate": low_rate,
        "high_rate": high_rate,
        "expected_buyers": expected_buyers,
        "min_buyers": min_buyers,
        "max_buyers": max_buyers,
    }


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show, add="+")
        widget.bind("<Leave>", self.hide, add="+")

    def show(self, _event=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 7
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tip,
            text=self.text,
            bg=COLORS["navy"],
            fg="white",
            font=("Microsoft YaHei UI", 9),
            padx=10,
            pady=7,
        ).pack()

    def hide(self, _event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None


class ParameterCard(tk.Frame):
    def __init__(
        self,
        master,
        title,
        symbol,
        description,
        variable,
        from_,
        to,
        resolution,
        command,
    ):
        super().__init__(master, bg=COLORS["white"], highlightthickness=1, highlightbackground=COLORS["line"])
        self.variable = variable
        self.command = command

        header = tk.Frame(self, bg=COLORS["white"])
        header.pack(fill="x", padx=18, pady=(15, 3))
        tk.Label(
            header,
            text=title,
            bg=COLORS["white"],
            fg=COLORS["navy"],
            font=("Microsoft YaHei UI", 11, "bold"),
        ).pack(side="left")
        badge = tk.Label(
            header,
            text=symbol,
            bg=COLORS["primary_light"],
            fg=COLORS["primary"],
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=2,
        )
        badge.pack(side="left", padx=8)
        ToolTip(badge, description)

        controls = tk.Frame(self, bg=COLORS["white"])
        controls.pack(fill="x", padx=18, pady=(5, 15))

        self.scale = tk.Scale(
            controls,
            variable=variable,
            from_=from_,
            to=to,
            resolution=resolution,
            orient="horizontal",
            showvalue=False,
            sliderlength=18,
            bd=0,
            highlightthickness=0,
            troughcolor="#DDE2F0",
            activebackground=COLORS["primary_dark"],
            bg=COLORS["white"],
            fg=COLORS["primary"],
            command=lambda _value: command(),
        )
        self.scale.pack(side="left", fill="x", expand=True, padx=(0, 14))

        entry_box = tk.Frame(controls, bg=COLORS["bg"], highlightthickness=1, highlightbackground=COLORS["line"])
        entry_box.pack(side="right")
        self.entry = tk.Entry(
            entry_box,
            textvariable=variable,
            width=6,
            justify="right",
            bd=0,
            bg=COLORS["bg"],
            fg=COLORS["navy"],
            insertbackground=COLORS["navy"],
            font=("Segoe UI", 12, "bold"),
        )
        self.entry.pack(side="left", padx=(9, 2), pady=7)
        tk.Label(
            entry_box,
            text="%",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(0, 8))
        self.entry.bind("<Return>", lambda _event: command())
        self.entry.bind("<FocusOut>", lambda _event: command())


class StyleTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME}  ·  v{APP_VERSION}")
        self.geometry("980x700")
        self.minsize(900, 650)
        self.configure(bg=COLORS["bg"])

        self.a_var = tk.DoubleVar(value=80.0)
        self.r_var = tk.DoubleVar(value=20.0)
        self.p1_var = tk.DoubleVar(value=3.0)
        self.status_var = tk.StringVar(value="参数已就绪")

        self._build_ui()
        self.after(80, self.calculate)

    def _build_ui(self):
        header = tk.Frame(self, bg=COLORS["navy"], height=102)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = tk.Label(
            header,
            text="款",
            bg=COLORS["primary"],
            fg="white",
            font=("Microsoft YaHei UI", 20, "bold"),
            width=2,
            height=1,
        )
        logo.pack(side="left", padx=(32, 16), pady=23)

        title_box = tk.Frame(header, bg=COLORS["navy"])
        title_box.pack(side="left", pady=19)
        tk.Label(
            title_box,
            text=APP_NAME,
            bg=COLORS["navy"],
            fg="white",
            font=("Microsoft YaHei UI", 22, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_box,
            text="服装选款 · 测试人流量计算工具",
            bg=COLORS["navy"],
            fg="#B7C1D8",
            font=("Microsoft YaHei UI", 10),
        ).pack(anchor="w", pady=(3, 0))

        formula_badge = tk.Label(
            header,
            text="科学测款  ·  数据决策",
            bg="#263554",
            fg="#D8DEEF",
            font=("Microsoft YaHei UI", 10),
            padx=15,
            pady=8,
        )
        formula_badge.pack(side="right", padx=32)

        body = tk.Frame(self, bg=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=30, pady=26)
        body.grid_columnconfigure(0, weight=5)
        body.grid_columnconfigure(1, weight=6)
        body.grid_rowconfigure(0, weight=1)

        left = tk.Frame(body, bg=COLORS["bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 13))

        tk.Label(
            left,
            text="设置测试参数",
            bg=COLORS["bg"],
            fg=COLORS["navy"],
            font=("Microsoft YaHei UI", 14, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        ParameterCard(
            left,
            "观测可信度",
            "a",
            "重复测试时，观察购买率落入目标范围的概率",
            self.a_var,
            50,
            99,
            1,
            self.calculate,
        ).pack(fill="x", pady=(0, 10))

        ParameterCard(
            left,
            "允许上下浮动",
            "r",
            "观察购买率相对于真实购买率允许的相对误差",
            self.r_var,
            1,
            80,
            1,
            self.calculate,
        ).pack(fill="x", pady=(0, 10))

        ParameterCard(
            left,
            "预计真实购买率",
            "p1",
            "根据公司历史经验预估的真实购买率",
            self.p1_var,
            0.1,
            50,
            0.1,
            self.calculate,
        ).pack(fill="x", pady=(0, 12))

        action_row = tk.Frame(left, bg=COLORS["bg"])
        action_row.pack(fill="x")
        tk.Button(
            action_row,
            text="恢复默认",
            command=self.reset_defaults,
            bd=0,
            bg="#E7EAF2",
            activebackground="#DCE0EA",
            fg=COLORS["navy"],
            activeforeground=COLORS["navy"],
            font=("Microsoft YaHei UI", 10),
            padx=18,
            pady=10,
            cursor=CURSOR_HAND,
        ).pack(side="left")
        tk.Button(
            action_row,
            text="立即计算",
            command=self.calculate,
            bd=0,
            bg=COLORS["primary"],
            activebackground=COLORS["primary_dark"],
            fg="white",
            activeforeground="white",
            font=("Microsoft YaHei UI", 10, "bold"),
            padx=22,
            pady=10,
            cursor=CURSOR_HAND,
        ).pack(side="right")

        right = tk.Frame(body, bg=COLORS["white"], highlightthickness=1, highlightbackground=COLORS["line"])
        right.grid(row=0, column=1, sticky="nsew", padx=(13, 0))

        result_header = tk.Frame(right, bg=COLORS["white"])
        result_header.pack(fill="x", padx=26, pady=(23, 0))
        tk.Label(
            result_header,
            text="计算结果",
            bg=COLORS["white"],
            fg=COLORS["navy"],
            font=("Microsoft YaHei UI", 14, "bold"),
        ).pack(side="left")
        self.status_label = tk.Label(
            result_header,
            textvariable=self.status_var,
            bg=COLORS["green_light"],
            fg=COLORS["green"],
            font=("Microsoft YaHei UI", 9),
            padx=10,
            pady=4,
        )
        self.status_label.pack(side="right")
        tk.Button(
            result_header,
            text="复制结果",
            command=self.copy_result,
            bd=0,
            bg=COLORS["navy"],
            activebackground="#263554",
            fg="white",
            activeforeground="white",
            font=("Microsoft YaHei UI", 9, "bold"),
            padx=12,
            pady=5,
            cursor=CURSOR_HAND,
        ).pack(side="right", padx=(0, 8))

        hero = tk.Frame(right, bg=COLORS["primary_light"])
        hero.pack(fill="x", padx=26, pady=18)
        tk.Label(
            hero,
            text="建议最低测试人流量",
            bg=COLORS["primary_light"],
            fg=COLORS["primary_dark"],
            font=("Microsoft YaHei UI", 10),
        ).pack(pady=(15, 0))
        number_line = tk.Frame(hero, bg=COLORS["primary_light"])
        number_line.pack(pady=(0, 13))
        self.m_label = tk.Label(
            number_line,
            text="--",
            bg=COLORS["primary_light"],
            fg=COLORS["primary"],
            font=("Segoe UI", 39, "bold"),
        )
        self.m_label.pack(side="left")
        tk.Label(
            number_line,
            text="人",
            bg=COLORS["primary_light"],
            fg=COLORS["primary_dark"],
            font=("Microsoft YaHei UI", 12, "bold"),
        ).pack(side="left", padx=(7, 0), pady=(20, 0))

        metrics = tk.Frame(right, bg=COLORS["white"])
        metrics.pack(fill="x", padx=26)
        metrics.grid_columnconfigure((0, 1), weight=1, uniform="metric")

        self.expected_value = self._metric_card(metrics, 0, 0, "预计购买人数", COLORS["green_light"], COLORS["green"])
        self.rate_value = self._metric_card(metrics, 0, 1, "p2 可信范围", COLORS["orange_light"], COLORS["orange"])
        self.buyers_value = self._metric_card(metrics, 1, 0, "对应购买人数", "#F1F4FA", COLORS["navy"], columnspan=2)

        formula_box = tk.Frame(right, bg="#F8F9FC", highlightthickness=1, highlightbackground=COLORS["line"])
        formula_box.pack(fill="x", padx=26, pady=(18, 10))
        tk.Label(
            formula_box,
            text="计算依据",
            bg="#F8F9FC",
            fg=COLORS["muted"],
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(anchor="w", padx=15, pady=(10, 2))
        self.formula_label = tk.Label(
            formula_box,
            text="m = z² × (1-p1) ÷ (r² × p1)",
            bg="#F8F9FC",
            fg=COLORS["navy"],
            font=("Cambria Math", 11),
        )
        self.formula_label.pack(anchor="w", padx=15, pady=(0, 10))

        footer = tk.Label(
            self,
            text="提示：本工具采用二项分布的正态近似进行测款样本量规划，结果向上取整。",
            bg=COLORS["bg"],
            fg=COLORS["muted"],
            font=("Microsoft YaHei UI", 9),
        )
        footer.pack(pady=(0, 14))

    def _metric_card(self, master, row, column, title, bg, fg, columnspan=1):
        outer = tk.Frame(master, bg=bg)
        outer.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            sticky="nsew",
            padx=(0 if column == 0 else 7, 0 if column == 1 else 7),
            pady=(0, 10),
        )
        tk.Label(
            outer,
            text=title,
            bg=bg,
            fg=COLORS["muted"],
            font=("Microsoft YaHei UI", 9),
        ).pack(pady=(11, 2))
        value = tk.Label(
            outer,
            text="--",
            bg=bg,
            fg=fg,
            font=("Microsoft YaHei UI", 14, "bold"),
        )
        value.pack(pady=(0, 12))
        return value

    def calculate(self):
        try:
            result = calculate_sample_size(self.a_var.get(), self.r_var.get(), self.p1_var.get())
        except (ValueError, tk.TclError) as exc:
            self.status_var.set("请检查参数")
            self.status_label.configure(bg="#FDECEF", fg=COLORS["red"])
            return

        self.result = result
        self.m_label.configure(text=f"{result['m']:,}")
        self.expected_value.configure(text=f"约 {result['expected_buyers']:.1f} 人")
        self.rate_value.configure(text=f"{result['low_rate'] * 100:.2f}% ～ {result['high_rate'] * 100:.2f}%")
        self.buyers_value.configure(text=f"{result['min_buyers']:,} ～ {result['max_buyers']:,} 人")
        self.formula_label.configure(
            text=f"z = {result['z']:.3f}    ·    m = {result['raw_m']:.2f}    ·    向上取整为 {result['m']:,}"
        )
        self.status_var.set("计算完成")
        self.status_label.configure(bg=COLORS["green_light"], fg=COLORS["green"])

    def reset_defaults(self):
        self.a_var.set(80.0)
        self.r_var.set(20.0)
        self.p1_var.set(3.0)
        self.calculate()

    def copy_result(self):
        self.calculate()
        if not hasattr(self, "result"):
            messagebox.showerror(APP_NAME, "参数有误，暂时无法复制结果。")
            return
        r = self.result
        text = (
            f"【{APP_NAME}计算结果】\n"
            f"观测可信度 a：{self.a_var.get():g}%\n"
            f"允许上下浮动 r：{self.r_var.get():g}%\n"
            f"预计真实购买率 p1：{self.p1_var.get():g}%\n"
            f"最低测试人流量：{r['m']:,} 人\n"
            f"预计购买人数：约 {r['expected_buyers']:.1f} 人\n"
            f"p2 可信范围：{r['low_rate'] * 100:.2f}% ～ {r['high_rate'] * 100:.2f}%\n"
            f"对应购买人数：{r['min_buyers']:,} ～ {r['max_buyers']:,} 人"
        )
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_var.set("结果已复制")


def main():
    app = StyleTestApp()
    app.mainloop()


if __name__ == "__main__":
    main()
