from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

def resize_image(image, base_width):
    # إعادة تحجيم الصورة بناءً على العرض الأساسي المطلوب
    width_percent = (base_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((base_width, height_size), Image.ANTIALIAS)

def add_texts(input_image_path, output_image_path):
    texts = ["عابد عبدالحميد", "08:11 2024/5/23", "24.62330921N 46.52916039E", "الظهرة اللبن"]
    base_width = 700

    # فتح الصورة الأصلية
    original_image = Image.open(input_image_path)

    # تعديل حجم الصورة إلى 700 بكسل عرضاً إذا كانت أصغر أو أكبر من ذلك
    if original_image.size[0] != base_width:
        original_image = resize_image(original_image, base_width)

    # إنشاء كائن للرسم على الصورة
    draw = ImageDraw.Draw(original_image)
    # تحميل خط الكتابة وتحديد حجمه
    font = ImageFont.truetype("arial.ttf", 36)
    
    # تحديد موقع النصوص في الزاوية اليمنى السفلية
    width, height = original_image.size
    padding = 10
    vertical_spacing = 10
    initial_y = height - padding

    for text in texts[::-1]:  # رسم النصوص من الأسفل إلى الأعلى
        # إعادة تشكيل النص العربي
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)

        # تحديد حجم النص
        textwidth, textheight = draw.textsize(bidi_text, font)
        
        x = width - textwidth - padding
        y = initial_y - textheight

        # إضافة الظل
        shadow_offset = 2
        draw.text((x + shadow_offset, y + shadow_offset), bidi_text, font=font, fill="black")
        # إضافة النص
        draw.text((x, y), bidi_text, font=font, fill="white")

        # تحديث الموضع الرأسي للنص التالي
        initial_y = y - vertical_spacing

    # حفظ الصورة المعدلة
    original_image.save(output_image_path)

# استخدام الدالة
input_image_path = 'test.jpg'
output_image_path = 'path_to_output_image.jpg'
add_texts(input_image_path, output_image_path)
