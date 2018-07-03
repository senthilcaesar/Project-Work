package edu.umb.cs.cs680.hw06;
import java.util.Comparator;

public class MileageComparator implements Comparator<Car> {

	//Sorting in Descending Order
	public int compare(Car c1, Car c2) { return (int) (c2.getMileage() - c1.getMileage()); }

}
