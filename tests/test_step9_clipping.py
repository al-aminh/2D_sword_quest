"""
# কী করছে: স্টেপ ৯-এর কোহেন-সাদারল্যান্ড ২ডি লাইন ক্লিপিং অ্যালগরিদম টেস্ট করছে।
# কেন লাগছে: ভিউপোর্টের সীমানায় রেখাংশের ট্রাইভিয়াল অ্যাকসেপ্ট, রিজেক্ট ও ইন্টারসেকশন যাচাই করতে।
# real world-এ এটা কোথায় দেখা যায়: কম্পিউটার গ্রাফিক্স পাইপলাইন ক্লিপিং টেস্ট স্যুয়িট।
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.physics.clipping import clip_line


def test_cohen_sutherland_clipping():
    xmin, ymin, xmax, ymax = 100.0, 100.0, 500.0, 400.0

    # ১. সম্পূর্ণ ভেতরের লাইন (Trivial Accept)
    res1 = clip_line(150.0, 150.0, 300.0, 300.0, xmin, ymin, xmax, ymax)
    assert res1 == (150.0, 150.0, 300.0, 300.0)

    # ২. সম্পূর্ণ বাইরের লাইন (Trivial Reject - বামে)
    res2 = clip_line(10.0, 150.0, 50.0, 300.0, xmin, ymin, xmax, ymax)
    assert res2 is None

    # ৩. আংশিক বাইরে থাকা লাইন (বাম সীমানা ভেদ করে ভেতরে প্রবেশ)
    res3 = clip_line(50.0, 200.0, 200.0, 200.0, xmin, ymin, xmax, ymax)
    assert res3 is not None
    assert abs(res3[0] - xmin) < 1e-4
    assert res3[1] == 200.0
    assert res3[2] == 200.0

    # ৪. দুই সীমানা ভেদ করা দীর্ঘ লাইন
    res4 = clip_line(50.0, 250.0, 600.0, 250.0, xmin, ymin, xmax, ymax)
    assert res4 is not None
    assert abs(res4[0] - xmin) < 1e-4
    assert abs(res4[2] - xmax) < 1e-4

    print("STEP 9 Line Clipping (Cohen-Sutherland algorithm) verified successfully!")


if __name__ == "__main__":
    test_cohen_sutherland_clipping()
