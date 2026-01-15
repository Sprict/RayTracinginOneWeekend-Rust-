mod color;
mod progress_bar;
mod ray;
mod vec3;

use color::to_rgb;
use progress_bar::SimpleProgressBar;
use ray::Ray;
use vec3::Vec3;

use image::RgbImage;

// Colorエイリアスがあれば良いが、とりあえずVec3を使う
type Color = Vec3;
type Point3 = Vec3;

/// レイの色を計算する
fn ray_color(r: &Ray) -> Color {
    // 背景（青〜白のグラデーション）
    let unit_direction = r.direction().unit_vector();
    let t = 0.5 * (unit_direction.y() + 1.0);
    // (1.0-t)*白 + t*青
    Color::new(1.0, 1.0, 1.0) * (1.0 - t) + Color::new(0.5, 0.7, 1.0) * t
}

fn main() {
    // Image dimensions
    let aspect_ratio = 16.0 / 9.0;
    let image_width = 400;
    let image_height = (image_width as f64 / aspect_ratio) as u32;

    // Create a new image buffer
    let mut img = RgbImage::new(image_width, image_height);

    // Camera
    let viewport_height = 2.0;
    let viewport_width = aspect_ratio * viewport_height;
    let focal_length = 1.0;

    let origin = Point3::new(0.0, 0.0, 0.0);
    let horizontal = Vec3::new(viewport_width, 0.0, 0.0);
    let vertical = Vec3::new(0.0, viewport_height, 0.0);
    let lower_left_corner =
        origin - horizontal / 2.0 - vertical / 2.0 - Vec3::new(0.0, 0.0, focal_length);

    // Initialize Progress Bar
    let mut bar = SimpleProgressBar::new(image_height as usize);

    // Render
    for y in 0..image_height {
        bar.update((y + 1) as usize);

        for x in 0..image_width {
            let u = x as f64 / (image_width - 1) as f64;
            // yは上から下だが、座標系は下が0なので反転
            let v = 1.0 - (y as f64 / (image_height - 1) as f64);

            let r = Ray::new(
                origin,
                lower_left_corner + horizontal * u + vertical * v - origin,
            );

            let pixel_color = ray_color(&r);

            // imageクレートのバッファに書き込み
            let pixel = img.get_pixel_mut(x, y);
            *pixel = color::to_rgb(&pixel_color);
        }
    }
    bar.finish();

    // Save the image
    match img.save("image.png") {
        Ok(_) => eprintln!("Image saved to image.png"),
        Err(e) => eprintln!("Error saving image: {}", e),
    }
}
