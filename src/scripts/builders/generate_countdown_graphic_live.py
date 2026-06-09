import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


def create_live_graphic():
    # 1. Calculate Countdown
    deadline = datetime(2026, 10, 5)
    today = datetime.now()
    diff = deadline - today
    days_remaining = max(0, diff.days + 1)

    # 2. Setup Image Canvas (1080 x 1080)
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # 3. Fonts
    try:
        font_bold_large = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 64
        )
        font_bold_med = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 36
        )
        font_bold_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 26
        )
        font_reg_med = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 26
        )
        font_reg_sm = ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 22
        )
    except OSError:
        # Fallbacks for Mac OS
        mac_font_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
        mac_font_reg = "/System/Library/Fonts/Supplemental/Arial.ttf"
        if os.path.exists(mac_font_path):
            font_bold_large = ImageFont.truetype(mac_font_path, 64)
            font_bold_med = ImageFont.truetype(mac_font_path, 36)
            font_bold_sm = ImageFont.truetype(mac_font_path, 26)
            font_reg_med = ImageFont.truetype(mac_font_reg, 26)
            font_reg_sm = ImageFont.truetype(mac_font_reg, 22)
        else:
            font_bold_large = font_bold_med = font_bold_sm = font_reg_med = (
                font_reg_sm
            ) = ImageFont.load_default()

    # 4. Drawing Layout
    # Top border line
    draw.rectangle([0, 0, width, 12], fill=(0, 0, 0))

    # Typography
    draw.text(
        (60, 50),
        "TEXAS GENERAL ELECTION — NOVEMBER 3, 2026",
        font=font_bold_sm,
        fill=(71, 85, 105),
    )
    draw.text((60, 90), "VOTER REGISTRATION", font=font_bold_large, fill=(0, 0, 0))
    draw.text(
        (60, 170),
        "HIDALGO COUNTY DEMOCRATIC PARTY (HDP) OUTREACH",
        font=font_bold_sm,
        fill=(71, 85, 105),
    )

    # Stat box
    draw.rounded_rectangle(
        [60, 230, 1020, 480],
        radius=15,
        fill=(241, 245, 249),
        outline=(0, 0, 0),
        width=3,
    )

    # Large stat days remaining
    stat_text = f"{days_remaining} DAYS REMAINING"
    bbox_stat = draw.textbbox((0, 0), stat_text, font=font_bold_large)
    stat_w = bbox_stat[2] - bbox_stat[0]
    draw.text(
        ((width - stat_w) // 2, 275), stat_text, font=font_bold_large, fill=(0, 0, 0)
    )

    sub_stat = "UNTIL THE OCTOBER 5, 2026 REGISTRATION DEADLINE"
    bbox_sub = draw.textbbox((0, 0), sub_stat, font=font_bold_sm)
    sub_w = bbox_sub[2] - bbox_sub[0]
    draw.text(
        ((width - sub_w) // 2, 370), sub_stat, font=font_bold_sm, fill=(15, 23, 42)
    )

    # Bullets
    bullets_y = 520
    # Bullet 1
    draw.ellipse([75, bullets_y + 25, 105, bullets_y + 55], fill=(0, 0, 0))
    draw.text((86, bullets_y + 28), "!", font=font_bold_sm, fill=(255, 255, 255))
    draw.text(
        (130, bullets_y + 10),
        "Voter Registration Deadline: October 5, 2026",
        font=font_bold_sm,
        fill=(0, 0, 0),
    )
    draw.text(
        (130, bullets_y + 45),
        "Applications must be received or postmarked by October 5. Texas does not allow",
        font=font_reg_sm,
        fill=(71, 85, 105),
    )
    draw.text(
        (130, bullets_y + 75),
        "online registration, so physical registration cards are required.",
        font=font_reg_sm,
        fill=(71, 85, 105),
    )

    # Bullet 2
    bullets_y2 = 680
    draw.ellipse([75, bullets_y2 + 25, 105, bullets_y2 + 55], fill=(0, 0, 0))
    draw.text((79, bullets_y2 + 28), "30", font=font_bold_sm, fill=(255, 255, 255))
    draw.text(
        (130, bullets_y2 + 10),
        "Texas 30-Day Requirement",
        font=font_bold_sm,
        fill=(0, 0, 0),
    )
    draw.text(
        (130, bullets_y2 + 45),
        "Under state law, you must be registered at least 30 days before Election Day",
        font=font_reg_sm,
        fill=(71, 85, 105),
    )
    draw.text(
        (130, bullets_y2 + 75),
        "in order to cast your ballot in this general election.",
        font=font_reg_sm,
        fill=(71, 85, 105),
    )

    # Bullet 3
    bullets_y3 = 820
    draw.ellipse([75, bullets_y3 + 25, 105, bullets_y3 + 55], fill=(0, 0, 0))
    draw.text((82, bullets_y3 + 28), "✓", font=font_bold_sm, fill=(255, 255, 255))
    draw.text(
        (130, bullets_y3 + 10),
        "Verify Registration Status Online",
        font=font_bold_sm,
        fill=(0, 0, 0),
    )
    draw.text(
        (130, bullets_y3 + 45),
        "Official Portal: VoteTexas.gov",
        font=font_bold_sm,
        fill=(0, 0, 0),
    )
    draw.text(
        (130, bullets_y3 + 80),
        "Confirm your status, update your home address, or download voter application form.",
        font=font_reg_sm,
        fill=(71, 85, 105),
    )

    # Divider & Footer
    draw.line([60, 990, 1020, 990], fill=(203, 213, 225), width=1)
    draw.text(
        (60, 1010),
        "HIDALGO COUNTY DEMOCRATIC PARTY (HDP)",
        font=font_bold_sm,
        fill=(71, 85, 105),
    )

    date_str = f"Live Update: {datetime.now().strftime('%B %d, %Y')}"
    bbox_date = draw.textbbox((0, 0), date_str, font=font_reg_sm)
    draw.text(
        (1020 - (bbox_date[2] - bbox_date[0]), 1012),
        date_str,
        font=font_reg_sm,
        fill=(71, 85, 105),
    )

    # Save file
    out_p = "texas_voter_registration_hdp_countdown.png"
    image.save(out_p, "PNG")
    print(
        f"Successfully generated live countdown graphic ({days_remaining} Days Remaining) saved at: {out_p}"
    )


if __name__ == "__main__":
    create_live_graphic()
