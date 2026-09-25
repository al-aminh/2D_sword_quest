"""
# কী করছে: কিউবিক বেজিয়ার কার্ভ ক্যালকুলেশন এবং বিভিন্ন স্মুথ ইজিং ম্যাথমেটিক্যাল ফাংশন সরবরাহ করে।
# কেন লাগছে: ইউআই-এর গোলাকার কোণা, তরবারির আর্ক ও প্ল্যাটফর্মের স্মুথ গতি তৈরিতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
"""

from typing import Tuple, List


# কী করছে: দুটি সংখ্যার মধ্যে লিনিয়ার ইন্টারপোলেশন (Lerp) করে।
# কেন লাগছে: সময়ের সাথে ধীরে ধীরে মান পরিবর্তনের মাধ্যমে স্মুথ ট্রানজিশন পেতে।
# real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিনের স্মুথ ক্যামেরা ড্যাম্পিং ও পজিশন ইন্টারপোলেশন।
def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


# কী করছে: কিউবিক বেজিয়ার সূত্রের সাহায্যে ৪টি কন্ট্রোল পয়েন্ট থেকে নির্দিষ্ট t সময়ের বিন্দু বের করে।
# কেন লাগছে: গাণিতিক নিখুঁত বক্ররেখা এবং মসৃণ গতিপথ তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
def evaluate_cubic_bezier(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    t: float
) -> Tuple[float, float]:
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t

    x = uuu * p0[0] + 3.0 * uu * t * p1[0] + 3.0 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3.0 * uu * t * p1[1] + 3.0 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)


# কী করছে: বেজিয়ার কার্ভ বরাবর নির্দিষ্ট সংখ্যক ইন্টারপোলেটেড বিন্দুর তালিকা তৈরি করে।
# কেন লাগছে: ওপেনজিএল প্রিমিটিভ দিয়ে গোলাকার কোণা বা আর্ক আঁকার জন্য ভার্টেক্স তৈরি করতে।
# real world-এ এটা কোথায় দেখা যায়: ভেক্টর গ্রাফিক্স সফটওয়্যার (যেমন Adobe Illustrator / SVG Path Renderer)।
def generate_bezier_points(
    p0: Tuple[float, float],
    p1: Tuple[float, float],
    p2: Tuple[float, float],
    p3: Tuple[float, float],
    segments: int = 8
) -> List[Tuple[float, float]]:
    points = []
    for i in range(segments + 1):
        t = i / float(segments)
        points.append(evaluate_cubic_bezier(p0, p1, p2, p3, t))
    return points


# কী করছে: কিউবিক ইজ-আউট গাণিতিক গতি গণনা করে।
# কেন লাগছে: অ্যানিমেশনের শুরুতে দ্রুত এবং শেষে মসৃণভাবে থামার আধুনিক ফিল দিতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    inv = 1.0 - t
    return 1.0 - (inv * inv * inv)


# কী করছে: কিউবিক ইজ-ইন-আউট স্মুথিং মান হিসাব করে।
# কেন লাগছে: প্ল্যাটফর্ম ও তরবারির সুইং শুরু ও শেষে প্রাকৃতিকভাবে ধীর গতি আনতে।
# real world-এ এটা কোথায় দেখা যায়: animation easing curves (e.g. CSS transitions, motion design tools), font/automotive design
def ease_in_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        return 4.0 * t * t * t
    p = -2.0 * t + 2.0
    return 1.0 - (p * p * p) / 2.0
