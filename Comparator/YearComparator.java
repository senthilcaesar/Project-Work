package edu.umb.cs.cs680.hw06;
import java.util.Comparator;

public class YearComparator implements Comparator<Car> {

	// Sorting in Ascending Order
	public int compare(Car c1, Car c2) { return c1.getYear() - c2.getYear(); }

}
