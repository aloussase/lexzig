pub fn factorial(n: i32) i32 {
    return if (n == 0) 1 else n * factorial(n - 1);
}

pub fn main() void {
    const std = @import("std");
    const result = factorial(10);

    std.debug.print("fact = {}", .{});
}
