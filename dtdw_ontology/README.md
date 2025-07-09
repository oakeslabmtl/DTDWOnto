## Pre-Requisites

Gradle requires:

1. [JDK 11 or higher](https://www.oracle.com/ca-en/java/technologies/downloads/)
2. [Fuseki](https://jena.apache.org/documentation/fuseki2/)
3. [openCAESER](https://www.opencaesar.io/)

You can verify by running on terminal:
```
java -version
```
which should report something like openjdk version `11.0.x` or higher

## (Optional) Set JAVA_HOME

Gradle uses the JDK it finds on your PATH or the one pointed to by `JAVA_HOME`

- `macOS/Linux`: in your shell profile (e.g. `~/.bash_profile` or `~/.zshrc`):

```
export JAVA_HOME="$(/usr/libexec/java_home)"
export PATH="$JAVA_HOME/bin:$PATH"
```

- Windows:
1. Open **System Properties** → **Environment Variables**
2. Create or edit `JAVA_HOME` to point to your JDK install (e.g. `C:\Program Files\Java\jdk-11.0.x`)
3. Add `%JAVA_HOME%\bin` to your Path variable

## Gradle Wrapper files

When you clone the project you will see in the `dtdw_ontology` directory: 

```
gradlew           ← Unix-shell script  
gradlew.bat       ← Windows batch script  
gradle/
    wrapper/
        gradle-wrapper.jar  
        gradle-wrapper.properties 
```
These files let you run a fixed `Gradle` version without installing `Gradle` yourself

## Run DTDeploy Ontology

1. **Ensure the wrapper is executable** for **macOS/Linux**

If you see Permission denied when running `./gradlew`, add execute permission:

```
chmod +x gradlew
```

2. **Available commands**

From the `/dtdw_ontology` directory, prefix every command with `./gradlew ` for **macOS/Linux**, or `gradlew.bat` for **Windows**:

| Task                                             | Command                                       | Description                                                              | 
|:-------------------------------------------------|:----------------------------------------------|:-------------------------------------------------------------------------|
| Clean + build                                    | `clean build`                                 | Deletes old outputs and compiles OML to OWL, runs reasoning, loads to Fuseki |
| Start Fuseki & load dataset                      | `start`                                       | Runs clean, build, startFuseki, owlLoad in order                         |
| Start Fuseki                                     | `startFuseki`                                 | Starts the headless Fuseki server                                        |
| Stop Fuseki                                      | `stopFuseki`                                  | Stops the headless Fuseki server                                         |
| Run SPARQL queries                               | `owlQuery`                                    | Executes queries under src/sparql                                        |
| Run reasoning only                               | `owlReason`                                   | Generates entailments via Openllet                                       |
| Check (invoked by CI)                            | `check`                                       | Runs owlReason as part of Gradle’s check lifecycle                       |
| Create OML ZIP artifact                          | `omlZip`                                      | Packages src/oml/**/*.oml into zip                                       |
| Publish to Maven (Sonatype)                      | `publishMavenPublicationToSonatypeRepository` | Signs & publishes artifact via Maven-Publish                             |

3. **Example:** To start the Fuseki server

- **macOS/Linux:** 
```
./gradlew start
```

- **Windows:**

```
gradlew.bat start
```

- The local Fuseki server starts at [http://localhost:3030/](http://localhost:3030/). 

### Troubleshooting

- `./gradlew: Permission denied`
Make sure you ran `chmod +x gradlew` on **macOS/Linux**

- **Gradle not found**
Always invoke via the wrapper scripts (`./gradlew or gradlew.bat`), never gradle, to guarantee the correct version

- **Wrong Java version**
Confirm `java -version` is ≥ 11, and that `JAVA_HOME` (if set) points to that JDK


With these commands you can reliably build, reason over, load, query, and publish your `DTKW` ontology dataset.
