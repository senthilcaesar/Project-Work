package edu.umb.cs.cs680.hw06;
import java.util.Comparator;

public class PriceComparator implements Comparator<Car> {

	// Sorting in Descending Order
	public int compare(Car c1, Car c2) { return c2.getPrice() - c1.getPrice(); }


}
