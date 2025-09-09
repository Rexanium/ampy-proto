module github.com/AmpyFin/ampy-proto/v2

go 1.23

require (
	github.com/AmpyFin/ampy-proto v0.0.0-00010101000000-000000000000
	google.golang.org/protobuf v1.36.8
)

// Optional but handy while developing locally (pre-push):
// This forces Go to resolve the module from the current directory.
replace github.com/AmpyFin/ampy-proto => .
