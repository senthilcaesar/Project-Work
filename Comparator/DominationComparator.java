package edu.umb.cs.cs680.hw06;

import java.util.Comparator;

public class DominationComparator implements Comparator<Car> {

	@Override
	public int compare(Car c1, Car c2) {
		return c1.getDominationCount() - c2.getDominationCount();
	}

}
