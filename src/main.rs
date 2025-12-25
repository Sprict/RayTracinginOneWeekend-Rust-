mod vec3;

use image::{Rgb, RgbImage};

fn main() {
    // Image dimensions
    let image_width = 256;
    let image_height = 256;

    // Create a new image buffer
    let mut img = RgbImage::new(image_width, image_height);

    // Render
    for y in 0..image_height {
        for x in 0..image_width {
            // ピクセル座標(y)から、論理座標(v)への変換
            // y=0 (画像上部) のとき、v=1.0 (計算上の上) にしたい
            let u = x as f64 / (image_width - 1) as f64;
            let v = 1.0 - (y as f64 / (image_height - 1) as f64); // ここで反転！

            // ... (色計算は u, v を使う) ...
            let r = u;
            let g = v;
            let b = 0.25_f64;

            let ir = (255.0 * r).clamp(0.0, 255.0) as u8;
            let ig = (255.0 * g).clamp(0.0, 255.0) as u8;
            let ib = (255.0 * b).clamp(0.0, 255.0) as u8;

            // 書き込みは物理座標 (x, y) に行う
            let pixel = img.get_pixel_mut(x, y);
            *pixel = Rgb([ir, ig, ib]);
        }
    }

    // Save the image
    match img.save("image.png") {
        Ok(_) => println!("Image saved to image.png"),
        Err(e) => eprintln!("Error saving image: {}", e),
    }
}
