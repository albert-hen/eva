import unittest

from src.expression.function_expression import FunctionExpression, \
    ExecutionMode
from src.models.storage.batch import FrameBatch


class FunctionExpressionTest(unittest.TestCase):
    def test_should_work_for_function_without_children_eval_mode(self):
        expression = FunctionExpression(lambda x: x)
        values = [1, 2, 3]
        actual = expression.evaluate(values)
        self.assertEqual(values, actual)

    def test_should_update_the_batch_with_outcomes_in_exec_mode(self):
        values = [1, 2, 3]
        expression = FunctionExpression(lambda x: values,
                                        mode=ExecutionMode.EXEC, name="test")
        expected_batch = FrameBatch(frames=[], info=None,
                                    outcomes={"test": [1, 2, 3]})
        input_batch = FrameBatch(frames=[], info=None)
        expression.evaluate(input_batch)
        self.assertEqual(expected_batch, input_batch)

    def test_should_throw_assert_error_when_name_not_provided_exec_mode(self):
        self.assertRaises(AssertionError,
                          lambda _=None:
                          FunctionExpression(lambda x: [],
                                             mode=ExecutionMode.EXEC),
                          )

    def test_when_function_executor_with_a_child_should_allow_chaining(self):
        expression = FunctionExpression(lambda x: x)
        child = FunctionExpression(lambda x: list(map(lambda t: t + 1, x)))
        expression.append_child(child)
        values = [1, 2, 3]
        actual = expression.evaluate(values)
        expected = [2, 3, 4]
        self.assertEqual(expected, actual)

    def test_should_update_temp_outcomes_when_is_temp_set_exec_mode(self):
        values = [1, 2, 3]
        expression = FunctionExpression(lambda x: values,
                                        mode=ExecutionMode.EXEC,
                                        name="test", is_temp=True)
        expected_batch = FrameBatch(frames=[], info=None,
                                    temp_outcomes={"test": [1, 2, 3]})
        input_batch = FrameBatch(frames=[], info=None)
        expression.evaluate(input_batch)
        self.assertEqual(expected_batch, input_batch)