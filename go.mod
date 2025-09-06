module github.com/yeonholee50/ampy-proto

go 1.23

require google.golang.org/protobuf v1.36.8

// Optional but handy while developing locally (pre-push):
// This forces Go to resolve the module from the current directory.
replace github.com/yeonholee50/ampy-proto => .
