"""
# কী করছে: কোহেন-সাদারল্যান্ড অ্যালগরিদম ব্যবহার করে ২ডি লাইন ক্লিপিং বাস্তবায়ন করে।
# কেন লাগছে: ক্যামেরার দৃশ্যমান উইন্ডোর বাইরে থাকা অংশ কেটে ফেলে রেন্ডারিং দ্রুত ও নির্ভুল করতে।
# real world-এ এটা কোথায় দেখা যায়: Line Clipping -> GPU rendering pipeline, viewport culling
"""

from typing import Tuple, Optional

# কোহেন-সাদারল্যান্ড রিজিওন কোড (৪-বিট ফ্ল্যাগ)
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000


# কী করছে: একটি বিন্দুর স্থানাঙ্ক দেখে তার ৪-বিট রিজিওন কোড গণনা করে।
# কেন লাগছে: বিন্দুটি ক্লিপিং উইন্ডোর ভেতরে নাকি বাইরে (বামে/ডানে/উপরে/নিচে) তা নির্ধারণ করতে।
# real world-এ এটা কোথায় দেখা যায়: ভিউপোর্ট বাউন্ডিং কোড জেনারেশন।
def compute_region_code(x: float, y: float, xmin: float, ymin: float, xmax: float, ymax: float) -> int:
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code


# কী করছে: কোহেন-সাদারল্যান্ড অ্যালগরিদমে রেখাংশকে ক্লিপিং বাউন্ডারি দিয়ে ছাঁটাই করে।
# কেন লাগছে: ওপেনজিএলের ডিফল্ট ক্লিপিংয়ের বাইরে সম্পূর্ণ ম্যানুয়াল অ্যালগরিদমিক ক্লিপিং প্রমাণ করতে।
# real world-এ এটা কোথায় দেখা যায়: Line Clipping -> GPU rendering pipeline, viewport culling
def clip_line(
    x1: float, y1: float, x2: float, y2: float,
    xmin: float, ymin: float, xmax: float, ymax: float
) -> Optional[Tuple[float, float, float, float]]:
    code1 = compute_region_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_region_code(x2, y2, xmin, ymin, xmax, ymax)

    while True:
        # ট্রাইভিয়াল অ্যাকসেপ্ট: সম্পূর্ণ রেখাংশ উইন্ডোর ভেতরে
        if (code1 | code2) == 0:
            return (x1, y1, x2, y2)

        # ট্রাইভিয়াল রিজেক্ট: সম্পূর্ণ রেখাংশ উইন্ডোর বাইরে একই পাশে
        if (code1 & code2) != 0:
            return None

        # যেকোনো একটি বাইরের বিন্দু বেছে নিয়ে ছেদবিন্দু নির্ণয়
        code_out = code1 if code1 != 0 else code2

        if code_out & TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif code_out & BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif code_out & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        else:  # LEFT
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin

        # নতুন ছেদবিন্দু দিয়ে প্রতিস্থাপন এবং কোড পুনর্বার হিসাব
        if code_out == code1:
            x1, y1 = x, y
            code1 = compute_region_code(x1, y1, xmin, ymin, xmax, ymax)
        else:
            x2, y2 = x, y
            code2 = compute_region_code(x2, y2, xmin, ymin, xmax, ymax)
