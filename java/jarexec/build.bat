javac -source 1.5 -target 1.5 -sourcepath src -d build\classes src\pkg\App.java
jar cfm build\jar\App.jar MANIFEST -C build\classes .
java -jar build\jar\App.jar
