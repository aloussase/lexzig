const std = @import("std");

pub fn main() void {
    // While Basic
    var i:i32 = 0;
    while (i < 10) {
        std.debug.print("i: {}\n", .{i});
        i += 1;
    }
    // While Loop Continue Expression
    var j:i32 = 1;
    while (j < 20) : ( j *= 2) {
        std.debug.print("j: {}\n", .{j});
    }
}