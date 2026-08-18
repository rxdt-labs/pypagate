=============
Why not RxPY?
=============

`ReactiveX for Python (RxPY) <https://rxpy.readthedocs.io/en/latest/index.html>`__ is probably the de facto standard for reactive programming in Python. RxPY and pypagate differ substantially in how reactivity is used and each have different use cases.

- RxPY focuses on processing streams of data.
- pypagate focuses on keeping everything up-to-date so you do not have to worry about manual updates.

If you do need to process data, pypagate has limited capabilities: It cannot, for instance, be used to easily filter elements of a stream. pypagate is largely about organization of programs by focusing on ergonomics. There is very little difference between managing normal variables and Term variables. Thus, what would require manual updates now can be done nearly for free.
