package edu.umb.cs.cs680.hw09;

import java.util.Date;
import java.util.LinkedList;

public class Directory extends FSElement {

	LinkedList<FSElement> list;


	public Directory(Directory parent, String name, String owner, Date created) {
		super(parent, name, owner, created);
			if(this.parent == null) {
			System.out.println(name + " directory created");
			}
			else {
			System.out.println(name + " directory created under " + this.parent.name);
			}
		this.size = 0;
		list = new LinkedList<FSElement>();
	
	}

	public void appendChild(FSElement e) {
		Date date = new Date();
		list.add(e);
		this.lastModified = date;
		
		if (this.parent != null) {
			this.parent.lastModified = date;
		}
	}
	
	public void getChildren() {
		for (FSElement object : list) {
			System.out.println(object.name);
        }
	}
	
	public int countFSElements() {
		return list.size();
	}
	
	public int getTotalSize() {
		int total = 0;
		for (FSElement object : list) {
			total += object.getSize();
        }
		return total;
	}

	public boolean isFile() {
		return false;
	}
	

	public String toString() {

		StringBuffer buffer = new StringBuffer();
		buffer.append("------------------------------------------\r\n");
		buffer.append("Directory: " + this.name + "\r\n");
		String parent = "null";
		if (this.parent != null)

		{
			parent = this.parent.name;
		}
		buffer.append("Parent: " + parent + "\r\n");
		buffer.append("Size: " + this.getSize() + "\r\n");
		buffer.append("Owner: " + this.owner + "\r\n");
		for (FSElement f : this.list) {
			buffer.append(f);
		}
		return buffer.toString();

	}
	
}
