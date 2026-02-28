package main

import "fmt"

func main() {
	var name string = "John"
	var age int = 30
	var salary float64 = 75000.50
	var isEmployed bool = true

	city := "New York"
	count := 100
	price := 19.99

	const PI float64 = 3.14159
	const COMPANY = "TechCorp"

	var (
		firstName = "Jane"
		lastName  = "Doe"
		score     = 95
	)

	var uninitializedInt int
	var uninitializedString string
	var uninitializedBool bool

	fmt.Printf("Name: %s\n", name)
	fmt.Printf("Age: %d\n", age)
	fmt.Printf("Salary: %.2f\n", salary)
	fmt.Printf("Employed: %t\n", isEmployed)
	fmt.Printf("City: %s\n", city)
	fmt.Printf("PI: %f\n", PI)
	fmt.Printf("Full Name: %s %s, Score: %d\n", firstName, lastName, score)
	fmt.Printf("Uninitialized: int=%d, string='%s', bool=%t\n",
		uninitializedInt, uninitializedString, uninitializedBool)
	fmt.Printf("%d, %d, %f", age, count, price)
}
