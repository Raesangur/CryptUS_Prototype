package main

import "os"

type Logger interface {
	Fatal(v ...interface{})
	Fatalf(format string, v ...interface{})
	Fatalln(v ...interface{})
	Print(v ...interface{})
	Printf(format string, v ...interface{})
	Println(v ...interface{})
	Panic(v ...interface{})
	Panicf(format string, v ...interface{})
}

type NullLogger struct{}

func (l NullLogger) Fatal(v ...interface{}) {
	os.Exit(1)
}

func (l NullLogger) Fatalf(format string, v ...interface{}) {
	os.Exit(1)
}

func (l NullLogger) Fatalln(v ...interface{}) {
	os.Exit(1)
}

func (l NullLogger) Print(v ...interface{})                 {}
func (l NullLogger) Printf(format string, v ...interface{}) {}
func (l NullLogger) Println(v ...interface{})               {}

func (l NullLogger) Panic(v ...interface{}) {
	panic(v)
}

func (l NullLogger) Panicf(format string, v ...interface{}) {
	panic(v)
}
