package app

import "testing"

func TestPing(t *testing.T) {
	result := Ping()
	expected := "pong"
	if result != expected {
		t.Errorf("Ping() = %q, want %q", result, expected)
	}
}

func TestGreet(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"Alice", "Alice", "Hello, Alice!"},
		{"Bob", "Bob", "Hello, Bob!"},
		{"Empty", "", "Hello, !"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Greet(tt.input)
			if result != tt.expected {
				t.Errorf("Greet(%q) = %q, want %q", tt.input, result, tt.expected)
			}
		})
	}
}
