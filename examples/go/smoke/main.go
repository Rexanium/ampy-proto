package main

import (
	"fmt"
	barspb "github.com/yeonholee50/ampy-proto/gen/go/ampy/bars/v1"
)

func main() {
	b := &barspb.Bar{}
	fmt.Println("Go import OK:", b)
}
