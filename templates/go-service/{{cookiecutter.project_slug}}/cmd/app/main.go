package main

import (
	"fmt"
	"{{cookiecutter.module_path}}/internal/app"
)

func main() {
	fmt.Println("{{cookiecutter.project_name}} is running!")
	fmt.Println(app.Ping())
	fmt.Println(app.Greet("World"))
}
