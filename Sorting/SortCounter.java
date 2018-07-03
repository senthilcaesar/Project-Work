import java.util.Scanner;
import java.io.*;

// CS210 Project 3 SortCounter class
// Bob Wilson 10/28/2015

public class SortCounter
{
  private static String dataFileName = null;
  private static int dataFileSize = 0;
  private static String [] dataArray;
  
  public static void main(String [] args) throws IOException
  {
    Scanner keyboard = new Scanner(System.in);
    String answer = null;
    
    do {
      System.out.println("Enter the data file name:");
      dataFileName = keyboard.next();
      
      // get the size of data file and create the sorting array
      dataFileSize = scanFile();
      dataArray = new String[dataFileSize];

      // and create the sorting and Searching object
      SortingAndSearching<String> sort = new SortingAndSearching<String>();

      // copy the data from the file to the array
      copyFile();

      // reset comparison counter
      sort.resetCompareCount();
 
      // use a selection sort
      sort.selectionSort(dataArray);

      // print results
      printResults("Selection Sort", sort.getCompareCount());
      
      // copy the data from the file to the array
      copyFile();

      // reset comparison counter
      sort.resetCompareCount();
 
      // use an insertion sort
      sort.insertionSort(dataArray);

      // print results
      printResults("Insertion Sort", sort.getCompareCount());
      // copy the data from the file to the array
      copyFile();

      // reset comparison counter
      sort.resetCompareCount();
 
      // use a bubble sort
      sort.bubbleSort(dataArray);

      // print results
      printResults("Bubble Sort", sort.getCompareCount());      // copy the data from the file to the array
      
      // copy the data from the file to the array
      copyFile();

      // reset comparison counter
      sort.resetCompareCount();
 
      // use a quick sort
      sort.quickSort(dataArray, 0, dataArray.length - 1);

      // print results
      printResults("Quick Sort", sort.getCompareCount());
      
      // copy the data from the file to the array
      copyFile();

      // reset comparison counter
      sort.resetCompareCount();
 
      // use a merge sort
      sort.mergeSort(dataArray, 0, dataArray.length - 1);

      // print results
      printResults("Merge Sort", sort.getCompareCount());
      System.out.println("Max Memory Use = " + sort.getMaxMemoryCount());
       
      System.out.println("Do you want to sort another data file?");
      answer = keyboard.next();
    } while (!answer.equals("n"));
    
    System.out.println("Done");
  }

  private static int scanFile() throws IOException
  {
      Scanner dataFile = new Scanner(new File(dataFileName));
      int index = 0;
      while (dataFile.hasNext()) {
        dataFile.next();
        index++;
      }
      return index;
  }
  private static void copyFile() throws IOException
  {
      Scanner dataFile = new Scanner(new File(dataFileName));
      int index = 0;
      while (dataFile.hasNext()) {
        dataArray[index++] = dataFile.next();
      }
  }

  private static void printResults(String algorithmName, int compareCount)
  {
      // for(String s : dataArray)
       // System.out.println(s);
          
      System.out.println("For file " + dataFileName + 
                         " of size " + dataFileSize +
                         ", the number of " + algorithmName + 
                         " comparisons is: " + compareCount);
  }
} /*201540*/