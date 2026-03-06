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

	loopsDemo()
	brnachingDemo()
}

func ifElseDemo() {
	score := 85

	if score >= 90 {
		fmt.Println("Grade: A")
	} else if score >= 80 {
		fmt.Println("Grade: B")
	} else {
		fmt.Println("Grade: F")
	}

	// if with initialization statement (scoped variable)
	if result := score >= 60; result {
		fmt.Printf("Pass %t\n", result)
	} else {
		fmt.Println("Fail")
	}

	age := 25
	hasLicense := true
	if age >= 18 && hasLicense {
		fmt.Println("Can drive")
	}
}

func loopsDemo() {
	// classic for loop
	for i := 0; i < 5; i++ {
		fmt.Printf(" Iteration %d\n", i)
	}

	// while-style
	count := 0
	for count < 3 {
		fmt.Printf(" Count; %d\n", count)
		count++
	}

	//infinite loop (use break to exit)
	fmt.Println("\nInfinite loop with break:")
	counter := 0
	for {
		fmt.Printf(" Counter: %d\n", counter)
		counter++
		if counter >= 3 {
			break
		}
	}

	// Range loop (foreach equivalent)
	fmt.Println("\nRange over slice:")
	lenguages := []string{"c#", "go", "python", "javascript"}
	for index, lang := range lenguages {
		fmt.Printf(" [%d] %s \n", index, lang)
	}

	fmt.Println("\nRange value only:")
	for _, lang := range lenguages {
		fmt.Printf(" %s\n", lang)
	}

	fmt.Println("\nRange over map:")
	scores := map[string]int{"alice": 95, "bob": 87, "carol": 92}
	for name, score := range scores {
		fmt.Printf(" %s: %d\n", name, score)
	}

	fmt.Println("\nRange over channel:")
	ch := make(chan int, 3)
	fmt.Printf("Sending 1 value to channel")
	ch <- 1
	fmt.Printf("Sending 2 value to channel")
	ch <- 2
	fmt.Printf("Sending 3 value to channel")
	ch <- 3
	close(ch)
	for num := range ch {
		fmt.Printf(" %d\n", num)
	}
}

func brnachingDemo() {
	fmt.Println("\nBreak example:")
	for i := 0; i < 10; i++ {
		if i == 5 {
			break
		}
		fmt.Printf("  %d\n", i)
	}

	fmt.Println("\nContinue example (skip even):")
	for i := 0; i < 10; i++ {
		if i%2 == 0 {
			continue
		}
		fmt.Printf(" %d\n", i)
	}
}
