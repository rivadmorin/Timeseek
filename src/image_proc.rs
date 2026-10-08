use image::{DynamicImage, GrayImage};

pub fn calculate_ssim(img1: &DynamicImage, img2: &DynamicImage) -> f64 {
    let gray1: GrayImage = img1.to_luma8();
    let gray2: GrayImage = img2.to_luma8();

    if gray1.dimensions() != gray2.dimensions() {
        return 0.0;
    }

    let (width, height) = gray1.dimensions();
    let total_pixels = (width * height) as f64;
    if total_pixels == 0.0 {
        return 1.0;
    }

    let k1 = 0.01;
    let k2 = 0.03;
    let l = 255.0;
    let c1 = (k1 * l) * (k1 * l);
    let c2 = (k2 * l) * (k2 * l);

    let mut sum1 = 0.0;
    let mut sum2 = 0.0;

    for (x, y, p1) in gray1.enumerate_pixels() {
        let p2 = gray2.get_pixel(x, y);
        sum1 += p1[0] as f64;
        sum2 += p2[0] as f64;
    }

    let mean1 = sum1 / total_pixels;
    let mean2 = sum2 / total_pixels;

    let mut var1 = 0.0;
    let mut var2 = 0.0;
    let mut cov = 0.0;

    for (x, y, p1) in gray1.enumerate_pixels() {
        let p2 = gray2.get_pixel(x, y);
        let diff1 = p1[0] as f64 - mean1;
        let diff2 = p2[0] as f64 - mean2;

        var1 += diff1 * diff1;
        var2 += diff2 * diff2;
        cov += diff1 * diff2;
    }

    var1 /= total_pixels;
    var2 /= total_pixels;
    cov /= total_pixels;

    ((2.0 * mean1 * mean2 + c1) * (2.0 * cov + c2))
        / ((mean1 * mean1 + mean2 * mean2 + c1) * (var1 + var2 + c2))
}
