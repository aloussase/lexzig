pub fn main() void {
    var x = switch (10) {
        0...1 => 20,
        10, 100 => @divExact(10, 10),
        else => 10,
    };
    _ = x;
}
