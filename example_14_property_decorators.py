class Temperature:
    """A class representing a temperature, demonstrating @property."""
    
    def __init__(self, celsius=0):
        # We store the internal value with an underscore to denote it's "private"
        self._celsius = celsius

    # The @property decorator turns a method into a "getter"
    @property
    def celsius(self):
        """Get the temperature in Celsius."""
        return self._celsius

    # The @setter decorator allows us to add validation when assigning a value
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero is not possible.")
        self._celsius = value

    # We can create computed properties that calculate values on the fly
    @property
    def fahrenheit(self):
        """Get the temperature in Fahrenheit."""
        return (self.celsius * 9 / 5) + 32

    # We can also have setters for computed properties
    @fahrenheit.setter
    def fahrenheit(self, value):
        # Convert back to Celsius and use the celsius setter (which includes validation)
        self.celsius = (value - 32) * 5 / 9

if __name__ == "__main__":
    # Create an instance
    temp = Temperature(25)
    
    # Accessing properties looks like accessing variables, not calling methods
    print(f"Current temp: {temp.celsius}°C / {temp.fahrenheit}°F")
    
    # Using the setter
    temp.fahrenheit = 100
    print(f"Changed to 100°F.")
    print(f"New temp: {temp.celsius:.2f}°C / {temp.fahrenheit}°F")
    
    # This will trigger our validation error!
    try:
        print("\nTrying to set temperature to absolute zero...")
        temp.celsius = -300
    except ValueError as e:
        print(f"Error caught: {e}")
