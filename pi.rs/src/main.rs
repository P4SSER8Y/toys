use clap::Parser;
use ibig::{ibig, ops::DivEuclid, IBig};
use indicatif;
use std::{ops::Mul, thread};

fn calc_x1(n: usize, bar: indicatif::ProgressBar) -> IBig {
    let t = n + 10;
    let mut x1 = ibig!(10).pow(t).mul(ibig!(4)).div_euclid(ibig!(5));
    let mut i = 3;
    let mut sum = x1.clone();
    while i < n * 2 {
        x1 = x1.div_euclid(IBig::from(-25));
        sum = sum + x1.clone().div_euclid(IBig::from(i));
        i += 2;
        bar.inc(1);
    }
    bar.finish();
    sum
}

fn calc_x2(n: usize, bar: indicatif::ProgressBar) -> IBig {
    let t = n + 10;
    let mut x2 = ibig!(10).pow(t).div_euclid(ibig!(-239));
    let mut i = 3;
    let mut sum = x2.clone();
    while i < n * 2 {
        x2 = x2.div_euclid(IBig::from(-57121));
        sum = sum + x2.clone().div_euclid(IBig::from(i));
        i += 2;
        bar.inc(1);
    }
    bar.finish();
    sum
}

#[derive(Parser, Debug)]
#[clap(author, version)]
struct Args {
    #[clap(value_parser)]
    base: usize,

    #[clap(value_parser)]
    size: usize,

    #[clap(value_parser, default_value_t = 1)]
    count: usize,
}

fn main() {
    let arg = Args::parse();
    let calc_length = arg.base + arg.size * arg.count;

    let bars = indicatif::MultiProgress::new();
    let f = |length: usize| {
        let bar = indicatif::ProgressBar::new(length.try_into().unwrap());
        bar.set_style(
            indicatif::ProgressStyle::default_bar().template("{percent}% {wide_bar} {per_sec}"),
        );
        bar.set_draw_rate(1);
        bar
    };
    let bar_x1 = bars.add(f(calc_length));
    let bar_x2 = bars.add(f(calc_length));

    let h_x1 = thread::spawn(move || calc_x1(calc_length, bar_x1));
    let h_x2 = thread::spawn(move || calc_x2(calc_length, bar_x2));
    let time = std::time::Instant::now();

    bars.join().unwrap();
    let pi = (h_x1.join().unwrap() + h_x2.join().unwrap()) * ibig!(4);
    let pi = pi.to_string();

    println!("used time: {:0.3}s", time.elapsed().as_secs_f32());
    for i in 0..arg.count {
        println!(
            "{}: {}",
            i,
            &pi[(arg.base + arg.size * i)..(arg.base + arg.size * i + arg.size)]
        );
    }
}
