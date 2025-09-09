// Package ampy provides access to all AmpyFin Protocol Buffer schemas.
//
// This package imports all generated protobuf packages, allowing users to
// install the entire ampy-proto library with a single command:
//
//	go get github.com/AmpyFin/ampy-proto/v2
//
// Individual packages can still be imported separately if needed:
//
//	import "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1"
package ampy

import (
	// Import all generated protobuf packages
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/bars/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/common/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/corporate_actions/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/fills/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/fundamentals/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/fx/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/metrics/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/news/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/orders/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/positions/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/signals/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/ticks/v1"
	_ "github.com/AmpyFin/ampy-proto/v2/gen/go/ampy/universe/v1"
)

// Version returns the current version of the ampy-proto library.
const Version = "2.0.6"
