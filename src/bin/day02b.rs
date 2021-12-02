use std::fs::File;
use std::io::{BufRead, BufReader};

type Error = Box<dyn std::error::Error>;
fn main() -> Result<(), Error> {
    let file = File::open("input/day02.txt")?;
    let reader = BufReader::new(file);
    let (mut x_pos, mut y_pos, mut aim) = (0, 0, 0);
    for line in reader.lines() {
        let line = line?;
        let (cmd, arg) = match &line.trim().split_whitespace().collect::<Vec<&str>>()[..] {
            [cmd, arg] => (cmd.to_owned(), arg.parse::<i32>()?),
            _ => panic!("invalid line: {}", line),
        };
        match cmd {
            "forward" => {
                x_pos += arg;
                y_pos += aim * arg;
            }
            "down" => aim += arg,
            "up" => aim -= arg,
            _ => panic!("invalid command: {}", cmd),
        }
    }
    println!("The product of the final position is {}", x_pos * y_pos);
    Ok(())
}
