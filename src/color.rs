use crate::vec3::Vec3;
use image::Rgb;

// 前提: Vec3構造体とColorエイリアス
type Color = Vec3;

/// Color(Vec3)をimage::Rgb<u8>に変換する
pub fn to_rgb(pixel_color: &Color) -> Rgb<u8> {
    let r = pixel_color.x();
    let g = pixel_color.y();
    let b = pixel_color.z();

    // [0, 1] の実数を [0, 255] の整数にマッピング
    let ir = (255.999 * r) as u8;
    let ig = (255.999 * g) as u8;
    let ib = (255.999 * b) as u8;

    Rgb([ir, ig, ib])
}

