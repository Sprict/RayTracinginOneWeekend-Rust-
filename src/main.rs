use image::{Rgb, RgbImage};

fn main() {
    // Image dimensions
    let image_width = 256;
    let image_height = 256;

    // Create a new image buffer
    let mut img = RgbImage::new(image_width, image_height);

    // Render
    for x in 0..image_width {
        for y in 0..image_height {
            let r = (x as f64 / (image_width - 1) as f64);
            let g = (y as f64 / (image_height - 1) as f64);
            let b = 0.25;

            let ir = (255.999 * r) as u8;
            let ig = (255.999 * g) as u8;
            let ib = (255.999 * b) as u8;

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
