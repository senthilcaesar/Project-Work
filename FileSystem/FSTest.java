package edu.umb.cs.cs680.hw09;

import java.util.Date;

import java.util.LinkedList;

import org.junit.Test;

import static org.junit.Assert.*;

public class FSTest {

	Date date = new Date();
	FileSystem base = FileSystem.getInstance();
	
	
	@Test
	public void test() {

	base.root = new Directory(null, "root", "root", date);
	Directory system = new Directory(base.root, "System", "caesar", date);
	File f1 = new File(system, "file_A", "caesar", date, 4);
	File f2 = new File(system, "file_B", "caesar", date, 4);
	File f3 = new File(system, "file_C", "caesar", date, 4);
	System.out.println("Total files and directories in System = " + system.countFSElements());
	System.out.println("Total size of System Directory = " + system.getTotalSize());
	System.out.println("System is a File = " + system.isFile());
	System.out.println("file_A is a file = " + f1.isFile());
	
	Directory home = new Directory(base.root, "Home", "caesar", date);
	Link l1 = new Link(home, "Link_X", "caesar", date, system);
	File f4 = new File(home, "file_D", "caesar", date, 4);
	
	Directory pictures = new Directory(home, "Pictures", "caesar", date);
	File f5 = new File(pictures, "file_E", "caesar", date, 4);
	File f6 = new File(pictures, "file_F", "caesar", date, 4);
	Link l2 = new Link(pictures, "Link_Y", "caesar", date, f5);
	
	
	base.showAllElements();
	
	}

}
