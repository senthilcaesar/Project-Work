package edu.umb.cs.cs680.hw06;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import org.junit.Test;

@SuppressWarnings("unused")
public class CarTest {

	List<Car> usedCars = new ArrayList<Car>();
	
	@Test
	public void test() {
		
		usedCars.add(new Car(200, 2006, 145.5));
		usedCars.add(new Car(40, 1971,  15.6));
		usedCars.add(new Car(300, 1995, 25.9));
		usedCars.add(new Car(100, 2000, 35.1));
		usedCars.add(new Car(500, 2014, 66.0));
		usedCars.add(new Car(800, 2018, 96.0));
		usedCars.add(new Car(100, 2000, 35.1));
		
		
		Collections.sort(usedCars, new PriceComparator());

		
		System.out.println("\nSorted by Price");
		System.out.println("------------------------");
		System.out.println("Price | Year | Mileage");
        for (int i=0; i<usedCars.size(); i++)
        	System.out.printf("%-8d%-8d%.2f\n", usedCars.get(i).getPrice(), usedCars.get(i).getYear(), usedCars.get(i).getMileage());
        
        Collections.sort(usedCars, new YearComparator());
        
		System.out.println("\nSorted by Year");
		System.out.println("------------------------");
		System.out.println("Price | Year | Mileage");
        for (int i=0; i<usedCars.size(); i++)
        	System.out.printf("%-8d%-8d%.2f\n", usedCars.get(i).getPrice(), usedCars.get(i).getYear(), usedCars.get(i).getMileage());
        
        Collections.sort(usedCars, new MileageComparator());
        
		System.out.println("\nSorted by Mileage");
		System.out.println("------------------------");
		System.out.println("Price | Year | Mileage");
        for (int i=0; i<usedCars.size(); i++)
            System.out.printf("%-8d%-8d%.2f\n", usedCars.get(i).getPrice(), usedCars.get(i).getYear(), usedCars.get(i).getMileage());

        
        System.out.println("\nComputing Domination Count for each Car");
        for (int i=0; i<usedCars.size(); i++) {
            usedCars.get(i).computeDominationCount(usedCars.get(i), usedCars);
            //System.out.println("Car " + i + " dominated by " + usedCars.get(i).getDominationCount() + " car");
        }
        
        Collections.sort(usedCars, new DominationComparator());
        
		System.out.println("\nSorted by Domination count");
		System.out.println("----------------------------------------");
		System.out.println("DominationCount | Price | Year | Mileage");
        for (int i=0; i<usedCars.size(); i++) 
        	System.out.printf("%-18d%-8d%-8d%.2f\n", usedCars.get(i).getDominationCount(), usedCars.get(i).getPrice(), usedCars.get(i).getYear(), usedCars.get(i).getMileage());
	
	}	
}
